"""One routing terminal per declared internal signal; retain every access shape."""
from collections import defaultdict
import re

from .supply_access import INSTANCE, CONNECTION


def split_pin(name):
    name=name.replace('<','[').replace('>',']')
    match=re.fullmatch(r'(.*)\[(\d+)\]',name)
    return (match[1],int(match[2])) if match else (name,None)


def pin_plan(cell_info, policy, supply_policy=None):
    """Resolve declarations against extracted pin shapes, never infer electrical aliases by voltage."""
    # Per-instance exposure must not regain hidden shapes via a shared alias.
    if (supply_policy or {}).get('scope') == 'all_signals':
        return {}
    result={}
    for master,metadata in cell_info.items():
        pins={p.replace('<','[').replace('>',']'):v for p,v in metadata.get('cell_pins',{}).items()}
        ports=defaultdict(dict)
        for pin in pins:
            port,index=split_pin(pin);ports[port][index]=pin
        parent={pin:pin for pin in pins}
        def find(pin):
            if parent[pin]!=pin:parent[pin]=find(parent[pin])
            return parent[pin]
        supply_families = set((supply_policy or {}).get('port_families', ()))
        def supply(pin):
            port, _ = split_pin(pin)
            return port.rsplit('_', 1)[0] in supply_families
        def join(a,b):
            # Preserve directional supply accesses for instance-level selection.
            if supply(a) or supply(b):
                return
            parent[find(b)]=find(a)
        skipped=[]
        def group(names,broadcast=False):
            names=[n for n in names if n in ports]
            if not names:return
            if broadcast:
                members=[pin for n in names for pin in ports[n].values()]
                for pin in members[1:]:join(members[0],pin)
            else:
                indices=set(ports[names[0]])
                if any(set(ports[n])!=indices for n in names[1:]):
                    skipped.append(dict(ports=names,reason='physical_lane_sets_differ'))
                    return
                for index in ports[names[0]]:
                    for name in names[1:]:join(ports[names[0]][index],ports[name][index])
        # Same-family rules are an explicit library contract, not a shared default.
        if policy.get('same_family_faces_connected'):
            families=defaultdict(list)
            aliases=policy.get('family_aliases',{})
            for name in ports:
                match=re.fullmatch(r'(.*)_([nsew])',name)
                if match:
                    family=aliases.get(match[1],match[1]);families[family].append(name)
            broadcast={aliases.get(n,n) for n in policy.get('broadcast_families',())}
            for family,names in families.items():group(names,family in broadcast)
        for declaration in policy.get('groups_by_master',{}).get(master,()):
            group(declaration['ports'],declaration.get('broadcast',False))
        mapping={pin:find(pin) for pin in pins}
        if any(pin!=root for pin,root in mapping.items()):
            shapes=defaultdict(list)
            for pin,root in mapping.items():
                shapes[root].append(dict(native_pin=pin,Layer=pins[pin]['Layer'],RECT=pins[pin]['RECT']))
            result[master]=dict(mapping=mapping,shapes=dict(shapes),skipped_groups=skipped)
    return result


def merged_pins(master,pins,plan):
    if master not in plan:return pins
    return {root:dict(Layer=shapes[0]['Layer'],RECT=shapes[0]['RECT'],access_shapes=shapes)
            for root,shapes in plan[master]['shapes'].items()}


def canonical_netlist(source,cell_info,plan):
    replacements=[];aliases_removed=0;instances=0;dummy=[]
    for match in INSTANCE.finditer(source):
        indent,master,instance,body=match.groups()
        if master not in plan:continue
        ports=defaultdict(dict)
        for raw in cell_info[master].get('cell_pins',{}):
            port,index=split_pin(raw);ports[port][index]=raw.replace('<','[').replace('>',']')
        destination={};original=0
        for port,expression in CONNECTION.findall(body):
            tokens=[t.strip() for t in expression.strip().strip('{}').split(',') if t.strip()]
            if not tokens:continue
            if port not in ports:raise ValueError(f'{instance}: unknown physical port {port}')
            indices=set(ports[port])
            expected=1 if indices=={None} else max(indices)+1
            if len(tokens)!=expected:
                raise ValueError(f'{instance}.{port}: expected {expected} bus positions, got {len(tokens)}; regenerate the full Verilog with preserved unused lanes')
            for offset,net in enumerate(reversed(tokens)):
                if net.startswith('__ashes_open_') or net.startswith('__ashes_supply_open_'):continue
                index=None if indices=={None} else offset
                if index not in ports[port]:
                    raise ValueError(f'{instance}.{port}: no physical pin for connected lane {offset}')
                original+=1
                target=plan[master]['mapping'][ports[port][index]]
                previous=destination.get(target)
                if previous is not None and previous!=net:
                    raise ValueError(f'{instance}: declared internal alias {target} is connected to different nets {previous!r} and {net!r}; no nets were shorted')
                destination[target]=net
        output=defaultdict(dict)
        for pin,net in destination.items():
            port,index=split_pin(pin);output[port][index]=net
        final_ports=defaultdict(set)
        for pin in plan[master]['shapes']:
            port,index=split_pin(pin);final_ports[port].add(index)
        connections=[]
        for port,values in output.items():
            indices=final_ports[port]
            if indices=={None}:expression=values[None]
            else:
                tokens=[]
                for index in range(max(indices)+1):
                    if index in values:tokens.append(values[index]);continue
                    serial=len(dummy)
                    while True:
                        name=f'__ashes_alias_open_{serial}'
                        if not re.search(r'\b'+name+r'\b',source) and name not in dummy:break
                        serial+=1
                    dummy.append(name);tokens.append(name)
                expression=tokens[0] if len(tokens)==1 else '{'+', '.join(reversed(tokens))+'}'
            connections.append(f'.{port}({expression})')
        aliases_removed+=original-len(destination);instances+=1
        replacements.append((match.start(),match.end(),f"{indent}{master} {instance} ({', '.join(connections)});"))
    result=source
    for start,stop,text in reversed(replacements):result=result[:start]+text+result[stop:]
    if dummy:
        header=re.search(r'\bmodule\s+\w+\s*\([^;]*\)\s*;',result,re.S)
        if not header:raise ValueError('Unsupported module header for unused alias bus lanes')
        result=result[:header.end()]+'\n'+''.join(f'wire {n};\n' for n in dummy)+result[header.end():]
    return result,dict(instances_processed=instances,duplicate_terminal_references_removed=aliases_removed,
                       masters=plan,isolated_lanes=len(dummy))
