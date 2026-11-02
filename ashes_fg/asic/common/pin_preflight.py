"""Physical pin diagnostics; independent of process and cell names."""
import logging
import re


def match_pin_labels(pin_names, pin_boxes, layer_map, pin_dt, cell_name=None, diagnostics=None, logger=None):
    assigned = {}
    for layer, name, x, y in pin_names:
        boxes = [b for b in pin_boxes if b[0] == layer]
        match = next((b for b in boxes if b[1] < x < b[3] and b[2] < y < b[4]), None)
        if match is not None:
            assigned[name] = {'Layer': layer_map[f'{layer},{pin_dt}']['pdk_name'],
                              'RECT': tuple(match[1:])}
            continue
        edge = any(b[1] <= x <= b[3] and b[2] <= y <= b[4] for b in boxes)
        reason = ('label_on_rectangle_edge' if edge else
                  'no_selected_pin_rectangles_on_layer' if not boxes else
                  'label_outside_selected_pin_rectangles')
        issue = dict(cell=cell_name, pin=name, layer=layer, selected_datatype=pin_dt,
                     coordinates=[x, y], reason=reason,
                     same_layer_rectangle_count=len(boxes))
        if diagnostics is not None:
            diagnostics.append(issue)
        (logger or logging.getLogger(__name__)).warning(
            'Unmatched physical pin: cell=%s pin=%s coordinates=(%s,%s) layer=%s '
            'selected_datatype=%s reason=%s same_layer_rectangles=%s',
            cell_name, name, x, y, layer, pin_dt, reason, len(boxes))
    return assigned


def validate_connected_abstract_ports(verilog, cell_info):
    """Validate named connections in ASHES-generated conventional Verilog.

    Checks port existence, including bus bases. Width/index validation is separate.
    This is deliberately not a general Verilog parser.
    """
    verilog = re.sub(r'/\*.*?\*/|//[^\n]*', '', verilog, flags=re.S)
    issues = []
    identifier = r'[A-Za-z_$][\w$]*'
    for match in re.finditer(r'(' + identifier + r')\s+(' + identifier + r')\s*\((.*?)\)\s*;', verilog, re.S):
        master, instance, body = match.groups()
        if master == 'module':
            continue
        ports = [(p, expression) for p, expression in
                 re.findall(r'\.(' + identifier + r')\s*\(([^()]*)\)', body)
                 if expression.strip()]
        if not ports:
            continue
        if master not in cell_info:
            issues.append(f'{instance} ({master}): no physical abstract metadata')
            continue
        pins = {p.replace('<', '[').replace('>', ']')
                for p in cell_info[master].get('cell_pins', {})}
        bases = {re.sub(r'\[\d+\]$', '', p) for p in pins}
        for port, _ in ports:
            if port not in bases:
                issues.append(f'{instance} ({master}): connected port {port!r} missing from physical abstract')
    if issues:
        raise ValueError('Connected-pin physical abstract preflight failed:\n- ' + '\n- '.join(issues))


from contextlib import contextmanager


@contextmanager
def pin_diagnostic_log(path):
    """Per-build logger: stream extraction details to disk, never the terminal."""
    logger = logging.Logger('ashes.physical_pin_extraction', level=logging.WARNING)
    logger.propagate = False
    handler = logging.FileHandler(path, mode='w')
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
    try:
        yield logger
    finally:
        logger.removeHandler(handler)
        handler.close()
        print(f'Pin extraction log: {path}')
