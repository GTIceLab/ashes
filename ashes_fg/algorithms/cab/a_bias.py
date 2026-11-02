"""Validate and bind JSON-selected extra A inputs without evaluating Python."""


def validate_connections(entries, count):
    """Validate zero-based indices within the A_col_biases section."""
    if not isinstance(entries, list):
        raise ValueError('A_bias_connections must be a list')
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Each A_bias_connections entry must be an object')
        column = entry.get('column')
        if type(column) is not int or not 0 <= column < count:
            raise ValueError('A bias column must be within 0 .. A_col_biases-1')
        if column in seen:
            raise ValueError(f'Duplicate A bias connection for column {column}')
        seen.add(column)
        target = entry.get('target')
        if not isinstance(target, dict):
            raise ValueError('A bias target must be an object')
        kind = target.get('kind')
        if kind == 'port':
            if (not isinstance(target.get('block'), str)
                    or not isinstance(target.get('port'), str)
                    or type(target.get('lane', 0)) is not int or target.get('lane', 0) < 0):
                raise ValueError('Port target requires block, native port, and nonnegative lane')
        elif kind == 'activation_rail':
            if type(target.get('group', 0)) is not int or target.get('group', 0) < 0:
                raise ValueError('Activation rail group must be a nonnegative integer')
            if not isinstance(target.get('rail'), str):
                raise ValueError('Activation rail target requires rail')
        elif kind == 'supply':
            if not isinstance(target.get('name'), str):
                raise ValueError('Supply target requires name')
        else:
            raise ValueError(f'Unsupported A bias target kind: {kind!r}')
    return tuple(entries)


def bind_connections(builder, columns, entries, *, blocks, activation_groups, aliases=None):
    """Resolve every target first, then connect lanes and export unused columns.

    `column` is relative to the extra/bias section, after power and C inputs.
    Native port names are used for coordinate-independent terminal lookup.
    """
    from ashes_fg.algorithms.system_build import port, pins
    from ashes_fg.algorithms.common import connect
    entries = validate_connections(list(entries), len(columns))
    resolved = []
    for entry in entries:
        target = entry['target']
        kind = target['kind']
        if kind == 'port':
            alias = (aliases or {}).get(target['block'] + '.' + target['port'], {})
            block, native = alias.get('block', target['block']), alias.get('port', target['port'])
            if block not in blocks:
                raise ValueError(f"Unknown A bias block: {block}")
            values = pins(port(blocks[block], native))
            lane = target.get('lane', 0)
            if lane >= len(values):
                raise ValueError(f"A bias target lane {lane} exceeds {target['block']}.{target['port']}")
            pin = values[lane]
        elif kind == 'activation_rail':
            group = target.get('group', 0)
            if group >= len(activation_groups) or target['rail'] not in activation_groups[group].rails:
                raise ValueError(f'Unknown activation rail target: {target}')
            pin = activation_groups[group].rails[target['rail']]
        else:
            if target['name'] not in builder.supplies:
                raise ValueError(f"Unknown A bias supply: {target['name']}")
            pin = builder.supplies[target['name']]
        resolved.append((entry['column'], pin))
    for column, pin in resolved:
        connect(columns[column], pin)
    used = {column for column, _ in resolved}
    builder.expose('A_bias', [pin for i, pin in enumerate(columns) if i not in used], 'N')
    return {entry['column']: entry['target'] for entry in entries}
