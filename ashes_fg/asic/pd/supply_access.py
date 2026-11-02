"""Select routing supply terminals from placement without changing the circuit model.

This opt-in export requires a declared same-net internal continuity assumption.
Legacy mode requires touching pin shapes. Boundary mode uses declared native
supply continuity across physically abutting cells, including array interiors.
Uncertain geometry and components without exposed access retain their connections.
"""
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import re


INSTANCE = re.compile(r'(?m)^([ \t]*)(\w+)\s+(\w+)\s*\((.*?)\)\s*;', re.S)
CONNECTION = re.compile(r'\.(\w+)\s*\(([^()]*)\)')


def placed_components(text, dbu=1000):
    """Read ASHES generated DEF placements, converting to parser coordinate units."""
    pattern = r'^\s*-\s+(\S+)\s+(\S+)[^;]*?\+\s+(?:PLACED|FIXED)\s*\(\s*(-?\d+)\s+(-?\d+)\s*\)\s+(\w+)'
    return {name: dict(master=master, x=int(x)*1000/dbu, y=int(y)*1000/dbu, orientation=orient)
            for name, master, x, y, orient in re.findall(pattern, text, re.M)}


def filter_supplies(verilog, placements, cell_info, policy, metal_layers, native_abutment=None):
    boundary_mode = policy.get('mode') == 'exposed_boundary'
    if policy.get('mode') not in ('exposed_abutment', 'exposed_boundary'):
        raise ValueError('Supply access mode must be exposed_abutment or exposed_boundary')
    if policy.get('same_net_terminals_connected_within_cell') is not True:
        raise ValueError('Exposed supply export requires an explicit within-cell continuity declaration')
    if boundary_mode and policy.get('same_net_supplies_connected_across_abutments') is not True:
        raise ValueError('Boundary supply export requires declared native continuity across abutments')
    all_signals = boundary_mode and policy.get('scope') == 'all_signals'
    if all_signals and policy.get('same_net_signals_connected_across_abutments') is not True:
        raise ValueError('All-signal boundary export requires declared native signal continuity')
    def real_net(token):
        return not token.startswith(('__ashes_open_', '__ashes_supply_open_', '__ashes_alias_open_'))
    nets = set(policy['nets'])
    families = set(policy['port_families'])
    overrides = policy.get('keep_access_overrides', [])
    for override in overrides:
        if 'net_bus' in override and (not isinstance(override['net_bus'], str) or not override['net_bus'].strip()):
            raise ValueError('net_bus overrides require a nonempty exact bus name')
        if (set(override) - {'instance', 'master', 'port', 'net', 'net_bus', 'reason'} or
                not any(isinstance(override.get(k), str) and override[k].strip()
                        for k in ('instance', 'master')) or
                not all(isinstance(override.get(k), str) and override[k].strip()
                        for k in ('port', 'reason'))):
            raise ValueError('Access overrides require exact instance or master, port and a reason; net is optional')
    tolerance = policy.get('tolerance_dbu', 0)
    if (isinstance(tolerance, bool) or not isinstance(tolerance, (int, float))
            or not math.isfinite(tolerance) or tolerance < 0):
        raise ValueError('Supply access tolerance must be nonnegative')
    rank = {name.lower(): i for i, name in enumerate(metal_layers)}
    boxes = {}
    for instance, placement in placements.items():
        master = cell_info.get(placement['master'], {})
        if placement['orientation'] != 'N' or tuple(master.get('origin', (0, 0))) != (0, 0):
            continue
        if 'width' not in master or 'height' not in master:
            continue
        x, y = placement['x'], placement['y']
        boxes[instance] = (x, y, x+master['width'], y+master['height'])

    def full_cover(intervals, lo, hi):
        cursor = lo
        for start, stop in sorted(intervals):
            if start > cursor+tolerance:
                return False
            cursor = max(cursor, stop)
            if cursor >= hi-tolerance:
                return True
        return False

    def exposed(instance, pin, rect, layer):
        own = boxes[instance]
        side = pin.rsplit('_', 1)[-1].upper()
        side = re.sub(r'\[\d+\]$', '', side)
        # Native directional labels are physical access-side declarations.
        if side not in ('N', 'S', 'E', 'W') or (not boundary_mode and layer.lower() not in rank):
            return True, 'unknown_access_side_or_layer', []
        axis, edge = {'N': (1, 3), 'S': (1, 1), 'E': (0, 2), 'W': (0, 0)}[side]
        transverse = 1-axis
        lo, hi = rect[transverse], rect[transverse+2]
        intervals, blockers = [], []
        for other, box in boxes.items():
            if other == instance:
                continue
            opposite = {'N': 1, 'S': 3, 'E': 0, 'W': 2}[side]
            if abs(box[opposite]-own[edge]) > tolerance:
                continue
            top = cell_info[placements[other]['master']].get('top_metal', '').lower()
            # Only block access on layers the neighboring macro actually blocks.
            if not boundary_mode and (top not in rank or rank[top] < rank[layer.lower()]):
                continue
            a, b = max(lo, box[transverse]), min(hi, box[transverse+2])
            if b > a:
                intervals.append((a, b))
                blockers.append(other)
        blocked = full_cover(intervals, lo, hi) if intervals else False
        reason = 'buried_at_abutment' if blocked else ('partial_coverage_preserved' if intervals else 'exposed_access')
        return not blocked, reason, blockers

    records, parsed, issues = [], [], []
    for match in INSTANCE.finditer(verilog):
        indent, master, instance, body = match.groups()
        if master == 'module':
            continue
        connections = []
        for connection in CONNECTION.finditer(body):
            port, expression = connection.groups()
            tokens = [t.strip() for t in expression.strip().strip('{}').split(',') if t.strip()]
            entry = dict(port=port, expression=expression, tokens=tokens, records={})
            connections.append(entry)
            family = port.rsplit('_', 1)[0]
            if not all_signals and (family not in families or not any(t in nets for t in tokens)):
                continue
            if instance not in boxes or placements[instance]['master'] != master:
                issues.append(dict(instance=instance, port=port, reason='unsupported_or_missing_placement'))
                continue
            metadata = cell_info[master]
            pins = {p.replace('<', '[').replace('>', ']'): v for p, v in metadata.get('cell_pins', {}).items()}
            indexed = {int(m.group(1)) for p in pins if (m := re.fullmatch(re.escape(port)+r'\[(\d+)\]', p))}
            if indexed and indexed != set(range(len(tokens))):
                issues.append(dict(instance=instance, port=port, reason='bus_width_or_index_mismatch_preserved'))
                continue
            for position, token in enumerate(tokens):
                if not real_net(token) or (not all_signals and token not in nets):
                    continue
                pin = f'{port}[{len(tokens)-1-position}]' if indexed else port
                shape = pins.get(pin)
                if not shape:
                    issues.append(dict(instance=instance, port=port, reason='missing_physical_pin_preserved'))
                    continue
                x, y = placements[instance]['x'], placements[instance]['y']
                r = shape['RECT']
                if len(r) != 4 or r[2] <= r[0] or r[3] <= r[1]:
                    issues.append(dict(instance=instance, port=port, reason='invalid_rectangle_preserved'))
                    continue
                rect = (r[0]+x, r[1]+y, r[2]+x, r[3]+y)
                access, reason, blockers = exposed(instance, pin, rect, shape['Layer'])
                declaration = (native_abutment or {}).get(instance)
                native_only = isinstance(declaration, str) or (isinstance(declaration, dict) and port in declaration['ports'])
                override = next((o for o in overrides if o.get('instance', instance) == instance
                                 and o.get('master', master) == master and o['port'] == port and o.get('net', token) == token
                                 and ('net_bus' not in o or token == o['net_bus'] or re.fullmatch(
                                     re.escape(o['net_bus']) + r'\[\d+\]', token))), None)
                if override and native_only:
                    raise ValueError(f'{instance}.{port}: boundary override cannot replace algorithm-native wiring')
                record = dict(instance=instance, master=master, pin=pin, net=token,
                              layer=shape['Layer'], rect=rect, exposed=access, reason=reason,
                              removed=False, blocking_neighbors=blockers, native_only=native_only,
                              override_reason=override['reason'] if override else None)
                entry['records'][position] = len(records)
                records.append(record)
        parsed.append((match, indent, master, instance, connections))

    # Within a cell, only same-net supply pins are grouped. No aliases are inferred.
    parent = {}
    def find(node):
        parent.setdefault(node, node)
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    def union(a, b):
        a, b = find(a), find(b)
        parent[a] = b
    for record in records:
        find((record['instance'], record['net']))
    if boundary_mode:
        # Native continuity belongs to the physical assembly, not just cells
        # that happened to emit a netlist terminal. Pinless pass-through cells
        # therefore cannot break an otherwise abutting assembly.
        physical_parent = {name: name for name in boxes}
        def physical_root(name):
            if physical_parent[name] != name:
                physical_parent[name] = physical_root(physical_parent[name])
            return physical_parent[name]
        items = list(boxes.items())
        for index, (name, first) in enumerate(items):
            for other, second in items[index+1:]:
                dx = min(first[2], second[2])-max(first[0], second[0])
                dy = min(first[3], second[3])-max(first[1], second[1])
                if ((abs(dx) <= tolerance and dy > tolerance) or
                        (abs(dy) <= tolerance and dx > tolerance)):
                    physical_parent[physical_root(name)] = physical_root(other)
        anchors = {}
        for record in records:
            key = (physical_root(record['instance']), record['net'])
            node = (record['instance'], record['net'])
            if key in anchors:
                union(node, anchors[key])
            else:
                anchors[key] = node
    for i, a in enumerate(records if not boundary_mode else []):
        ar = a['rect']
        for b in records[i+1:]:
            if a['instance'] == b['instance'] or a['net'] != b['net']:
                continue
            if a['layer'] != b['layer']:
                continue
            br = b['rect']
            dx, dy = min(ar[2], br[2])-max(ar[0], br[0]), min(ar[3], br[3])-max(ar[1], br[1])
            if dx >= -tolerance and dy >= -tolerance and (dx > tolerance or dy > tolerance):
                union((a['instance'], a['net']), (b['instance'], b['net']))
    anchored = {find((r['instance'], r['net'])) for r in records
                if (r['reason'] == 'exposed_access' or r.get('override_reason')) and not r['native_only']}
    contract_assemblies = all_signals and policy.get('native_assembly_routing') == 'boundary_only'
    internal_nets = set()
    declared_native_nets = nets | {record['net'] for record in records if record['native_only']}
    if contract_assemblies:
        external = set()
        for high, low, name in re.findall(
                r'\b(?:input|output|inout)\s*(?:\[(\d+):(\d+)\])?\s*(\w+)\s*;', verilog):
            if high:
                external.update(f'{name}[{i}]' for i in range(int(low), int(high)+1))
            else:
                external.add(name)
        net_components = defaultdict(set)
        for record in records:
            net_components[record['net']].add(physical_root(record['instance']))
        internal_nets = {net for net, components in net_components.items()
                         if len(components) == 1 and net not in external and net in declared_native_nets}
    no_access = []
    if boundary_mode:
        components = defaultdict(list)
        for record in records:
            components[find((record['instance'], record['net']))].append(record)
        for root, members in components.items():
            if members[0]['net'] in internal_nets:
                continue
            if all_signals and members[0]['net'] not in nets and all(m['native_only'] for m in members):
                continue
            if root not in anchored:
                no_access.append(dict(net=members[0]['net'],
                    instances=sorted({m['instance'] for m in members}),
                    reason='no_proven_exposed_supply_access'))
    for record in records:
        if record['native_only'] or record.get('override_reason'):
            continue
        if not record['exposed']:
            if find((record['instance'], record['net'])) in anchored:
                record['removed'] = True
            else:
                record['reason'] = 'buried_but_no_proven_exposed_path_preserved'

    if all_signals:
        # Raw physical faces stay separate. A single exposed routing endpoint
        # represents each cell/net's native internal connection; the remaining
        # equivalent faces must not become extra routed ties.
        selected = set()
        for record in sorted(records, key=lambda r: not bool(r.get('override_reason'))):
            if record['native_only'] or record['removed'] or (not record['exposed'] and not record.get('override_reason')):
                continue
            node = (record['instance'], record['net'])
            if node in selected and not record.get('override_reason'):
                record['removed'] = True
                record['reason'] = 'same_net_exposed_copy_uses_selected_access'
            else:
                selected.add(node)

    if contract_assemblies:
        # Contract native wiring without altering the full logical netlist.
        candidates = defaultdict(list)
        for record in records:
            if not record['native_only']:
                candidates[physical_root(record['instance']), record['net']].append(record)
        for (_, net), members in candidates.items():
            if net not in declared_native_nets:
                continue
            forced = [r for r in members if r.get('override_reason')]
            if net in internal_nets and not forced:
                for record in members:
                    record['removed'] = True
                    record['reason'] = 'native_internal_assembly_connection'
                continue
            available = [r for r in members if not r['removed'] and r['exposed']]
            # The explicit preservation override permits one fallback access,
            # never every buried contact in the assembly.
            if not available and not forced and policy.get('on_no_exposed_access') == 'preserve':
                available = [r for r in members if not r['removed']]
            keep = {id(r) for r in forced or available[:1]}
            for record in available[:1]:
                if not record['exposed'] and not forced:
                    record['override_reason'] = 'on_no_exposed_access=preserve: selected one unexposed native-assembly access'
            for record in members:
                if id(record) not in keep:
                    record['removed'] = True
                    record['reason'] = 'native_assembly_uses_selected_boundary_access'

    dummy, replacements = [], []
    serial = 0
    for match, indent, master, instance, connections in parsed:
        changed, output = False, []
        for entry in connections:
            remove = {pos for pos, i in entry['records'].items() if records[i]['removed']}
            if not remove:
                output.append(f".{entry['port']}({entry['expression']})")
                continue
            changed = True
            if len(remove) == len(entry['tokens']):
                continue
            tokens = list(entry['tokens'])
            for position in sorted(remove):
                while True:
                    name = f'__ashes_supply_open_{serial}'
                    serial += 1
                    if re.search(r'\b'+re.escape(name)+r'\b', verilog) is None:
                        break
                dummy.append(name)
                tokens[position] = name
            expression = tokens[0] if len(tokens) == 1 else '{'+', '.join(tokens)+'}'
            output.append(f".{entry['port']}({expression})")
        if changed:
            replacements.append((match.start(), match.end(), f"{indent}{master} {instance} ({', '.join(output)});"))
    result = verilog
    for start, stop, replacement in reversed(replacements):
        result = result[:start]+replacement+result[stop:]
    if dummy:
        header = re.search(r'\bmodule\s+\w+\s*\([^;]*\)\s*;', result, re.S)
        if not header:
            raise ValueError('Cannot declare isolated supply bus lanes: unsupported module header')
        declarations = '\n'+''.join(f'wire {name};\n' for name in dummy)
        result = result[:header.end()]+declarations+result[header.end():]
    report = dict(policy=policy, candidate_terminals=len(records),
                  removed_terminals=sum(r['removed'] for r in records),
                  removed_by_net=dict(Counter(r['net'] for r in records if r['removed'])),
                  isolated_bus_lanes=len(dummy), terminals=records, preserved_issues=issues,
                  no_exposed_access=no_access,
                  native_internal_nets=sorted(internal_nets),
                  access_overrides=[dict(instance=r['instance'], pin=r['pin'], net=r['net'],
                      reason=r['override_reason']) for r in records if r.get('override_reason')])
    return result, report


def apply_supply_access(netlist_path, def_path, cell_info, policy, metal_layers, dbu, report_path, native_abutment=None, routing_pin_plan=None):
    netlist_path, report_path = Path(netlist_path), Path(report_path)
    source = netlist_path.read_text()
    placements = placed_components(Path(def_path).read_text(), dbu)
    for instance, selection in (native_abutment or {}).items():
        master = selection if isinstance(selection, str) else selection['master']
        if placements.get(instance, {}).get('master') != master:
            raise ValueError(f'{instance}: native-abutment export has no matching physical placement')
    from .routing_export import omit_native_abutment_connections
    if policy and policy.get('mode') == 'exposed_boundary':
        # Hidden native contacts still establish continuity through the assembly,
        # but cannot count as external supply anchors.
        filtered, report = filter_supplies(source, placements, cell_info, policy,
                                           metal_layers, native_abutment=native_abutment)
        result, abutment_report = omit_native_abutment_connections(filtered, native_abutment or {})
    else:
        routing_source, abutment_report = omit_native_abutment_connections(source, native_abutment or {})
        if policy:
            result, report = filter_supplies(routing_source, placements, cell_info, policy, metal_layers)
        else:
            result, report = routing_source, dict(candidate_terminals=0, removed_terminals=0,
                                                 terminals=[], preserved_issues=[])
    if routing_pin_plan:
        from .multi_access import canonical_netlist
        result, alias_report = canonical_netlist(result, cell_info, routing_pin_plan)
        report['multi_access_pins'] = alias_report
    report['native_abutment_export'] = abutment_report
    if report.get('no_exposed_access') and (policy or {}).get('on_no_exposed_access') == 'preserve':
        report['error_overrides'] = [dict(item, override='on_no_exposed_access=preserve')
                                     for item in report['no_exposed_access']]
    netlist_path.with_suffix('.full.v').write_text(source)
    report_path.write_text(json.dumps(report, indent=2)+'\n')
    report_path.with_suffix('.log').write_text(
        f"Routing access candidates: {report['candidate_terminals']}\n"
        f"Removed routing terminals: {report['removed_terminals']}\n"
        f"Native-abutment terminal omissions: {abutment_report['removed_terminals']}\n"
        f"Internal access aliases consolidated: {report.get('multi_access_pins', {}).get('duplicate_terminal_references_removed', 0)}\n"
        'Full logical export is preserved in inputs/*.full.v.\n'
        f"Routing assemblies without exposed access: {len(report.get('no_exposed_access', []))}\n"
        'See JSON for blocking neighbors and preserved uncertain/partial accesses.\n'
        + ''.join(f"OVERRIDE: {item['instance']}.{item['pin']} net={item['net']}: {item['reason']}\n"
                  for item in report.get('access_overrides', []))
        + ''.join(f"OVERRIDE: {item['override']} net={item['net']} instances={', '.join(item['instances'])}\n"
                  for item in report.get('error_overrides', []))
        + ''.join(f"WARNING: {item['net']} has no proven exposed access: {', '.join(item['instances'])}; contacts preserved.\n"
                  for item in report.get('no_exposed_access', [])))
    behavior = (policy or {}).get('on_no_exposed_access', 'error')
    if behavior not in ('error', 'preserve'):
        raise ValueError('on_no_exposed_access must be error or preserve')
    if report.get('no_exposed_access') and behavior == 'error':
        raise ValueError(f'Routing assemblies lack exposed access; see {report_path}')
    netlist_path.write_text(result)
    print(f'Routing access report: {report_path}')
