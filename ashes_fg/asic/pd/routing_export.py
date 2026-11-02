"""Omit algorithm-declared native contacts from routing, preserving placement."""


def native_abutment_instances(circuit):
    result = {}
    for number, island in enumerate(circuit.Islands):
        for cell in island.instances:
            ports = [p.native_name for p in getattr(cell, 'ports', ()) if getattr(p, 'native_abutment', False)]
            whole = getattr(cell, 'routing_export', 'explicit') == 'native_abutment'
            pin_ports = [p for p in getattr(cell, 'ports', ())
                         if any(getattr(pin, 'native_abutment', False) for pin in p.pins)]
            if not whole and not ports and not pin_ports:
                continue
            if cell.isDecoder():
                raise ValueError('Native-abutment instance export does not support legacy MUX naming')
            location = island.getLocation(cell)
            row, col = ((int(location[0][0]), int(location[1][0]))
                        if isinstance(location, tuple) and len(location[0]) else (0, 0))
            rows, cols = (max(1, int(n)) for n in cell.dim)
            for r in range(rows):
                for c in range(cols):
                    name = (f'I_{number}_{row+r}_{col+c}_{r}_{c}' if rows > 1 or cols > 1
                            else f'I_{number}_{row}_{col}')
                    selected = list(ports)
                    for port in pin_ports:
                        width = int(port.numPins())
                        index = r if port.location in ('E', 'W') else c
                        members = port.pins[index*width:(index+1)*width]
                        if members and all(getattr(pin, 'native_abutment', False) for pin in members):
                            selected.append(port.native_name)
                    if whole or selected:
                        result[name] = cell.name if whole else dict(master=cell.name, ports=selected)
    return result


def omit_native_abutment_connections(source, declared):
    from .supply_access import INSTANCE, CONNECTION
    replacements, records, found = [], [], set()
    for match in INSTANCE.finditer(source):
        indent, master, instance, body = match.groups()
        if instance not in declared:
            continue
        selection = declared[instance]
        selected_ports = None if isinstance(selection, str) else set(selection['ports'])
        expected_master = selection if isinstance(selection, str) else selection['master']
        if master != expected_master:
            raise ValueError(f'{instance}: native-abutment export master differs from the model')
        found.add(instance)
        matches = list(CONNECTION.finditer(body))
        selected = [m for m in matches if selected_ports is None or m.group(1) in selected_ports]
        connections = [m.groups() for m in selected]
        terminals = sum(len([t for t in expr.strip().strip('{}').split(',') if t.strip()])
                        for _, expr in connections)
        records.append(dict(instance=instance, master=master,
                            removed_port_connections=len(connections),
                            removed_terminals=terminals,
                            reason='native_abutment', removed_ports=[p for p, _ in connections]))
        kept = [m.group(0) for m in matches if m not in selected]
        replacements.append((match.start(), match.end(), f'{indent}{master} {instance} (' + ', '.join(kept) + ');'))
    missing = set(declared) - found
    if missing:
        raise ValueError(f'Native-abutment instances missing from routing export: {sorted(missing)}')
    result = source
    for start, stop, replacement in reversed(replacements):
        result = result[:start]+replacement+result[stop:]
    return result, dict(instances=records, instance_count=len(records),
                        removed_terminals=sum(r['removed_terminals'] for r in records))
