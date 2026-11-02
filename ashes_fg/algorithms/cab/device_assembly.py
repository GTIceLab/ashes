"""Compose ordered CAB signal devices and registered activation support cells."""
from types import SimpleNamespace
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ashes_fg.asic.placement.companion_groups import register_companion_group
from ashes_fg.algorithms.system_build import pins, port
from ashes_fg.algorithms.common import connect


def layout_activation_devices(context):
    """Keep native left-to-right assembly order under either staging convention.

    Use the existing ASHES custom-island layout protocol. It adds physical
    companions afterward; this callback places only its declared body cells.
    No programming circuitry is generated for the activation devices.
    """
    coordinates = next(iter(context.entries.values()))[2]
    swapped = coordinates != 'xy'
    boxes = {}
    cursor = 0
    for index, descriptor in sorted(context.entries.items(), key=lambda item: item[1][1]):
        info = context.cells[context.island['items'][index]['name']]
        width, height = (info['height'], info['width']) if swapped else (info['width'], info['height'])
        boxes[index] = [cursor, 0, cursor + width, height]
        cursor += width
    if swapped:
        return {index: [box[1], cursor - box[2], box[3], cursor - box[0]]
                for index, box in boxes.items()}
    return boxes


def build_devices(builder, descriptors, profiles):
    """Create device bodies; support cells add no functional input/output lanes.

    Activation members explicitly share native W/E control and bias rails.
    A requested bottom cell closes the group. Physical companions are owned
    by the shared ASHES pass, preserving the legacy EdgeL/body/Bot/EdgeL recipe.
    """
    owner = builder.island('Devices') if descriptors else None
    grid = AlgorithmGrid.for_process(owner, builder.process_coordinates) if owner else None
    instances, inputs, outputs, activation_groups = [], [], [], []
    active = []
    slot = 0

    def finish_activation():
        nonlocal active
        if not active:
            return
        group_index = len(activation_groups)
        rails = {}
        for family in ('WTA', 'WTA_B', 'Vg_pFET', 'Vg_p', 'Vg_m', 'Vc'):
            wire = ac.Wire(builder.circuit)
            for member in active:
                for side in ('w', 'e'):
                    native = port(member, family + '_' + side)
                    if family in ('Vg_pFET', 'Vg_p', 'Vg_m'):
                        native.native_abutment = True
                    for pin in pins(native):
                        connect(pin, wire)
            rails[family] = wire
        # Explicit continuity makes the netlist agree with abutting geometry.
        for family in ('GND', 'VDD'):
            for member in active:
                for side in ('w', 'e'):
                    builder.common(family, port(member, family + '_' + side))
        register_companion_group(owner, active, supplies=builder.supplies)
        activation_groups.append(SimpleNamespace(members=tuple(active), rails=rails))
        active = []

    for descriptor in descriptors:
        if descriptor.assembly != 'activation':
            finish_activation()
        metadata = profiles.get(descriptor.std_cell, {})
        for instance in range(descriptor.count):
            body = getattr(builder.cells, descriptor.std_cell)(builder.circuit, owner)
            body.markAbut()
            grid.place(body, (slot, 0))
            slot += grid.shape(body)[1]
            instances.append(body)
            builder.static(body)
            if descriptor.assembly == 'activation':
                active.append(body)
            for identifiers, destination in ((descriptor.inputs, inputs), (descriptor.outputs, outputs)):
                for identifier in identifiers:
                    native, lane = identifier[:-1].rsplit('[', 1)
                    destination.append(port(body, native)[int(lane)])
            used = {identifier.split('[')[0] for identifier in descriptor.inputs + descriptor.outputs}
            shared = set(metadata.get('static_ports', ())) if descriptor.assembly == 'activation' else set()
            # Preserve the legacy unconnected bottom-bias pin. Other auxiliary
            # signal/bias ports remain exported per instance as before.
            omitted = set(metadata.get('legacy_unconnected_ports', ()))
            for p in body.ports:
                family = p.native_name.rsplit('_', 1)[0]
                if (p.native_name not in used | shared | omitted
                        and family not in ('GND', 'VDD', 'VINJ', 'VTUN')):
                    builder.expose(f'{descriptor.key}_{instance}_{p.native_name}', p, 'N')
        if descriptor.role == 'support':
            finish_activation()
    finish_activation()
    if activation_groups:
        from ashes_fg.asic.peripherals.fg_generation import Generated
        for index, body in enumerate(instances):
            body.fg_geometry = ('activation_body', index, builder.process_coordinates)
        owner.fg_generated = Generated(None, None, instances=tuple(instances),
                                       layout=layout_activation_devices)
    return SimpleNamespace(instances=instances, inputs=inputs, outputs=outputs,
                           activation_groups=activation_groups)
