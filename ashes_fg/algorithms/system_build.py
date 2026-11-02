"""Reusable wiring and circuit-construction helpers for ASHES system designs.

No CAB topology is encoded here. Each CircuitBuilder owns one circuit's
registries; its caller selects shared-net policies and matrix cell capacities.
"""
import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
from ashes_fg.asic.peripherals.fg_extensions import generate_drain_extension
from .common import native_port, connect


def pins(value):
    """Return a flat, ordered list of individual pins.

    Recursively unpack lists and tuples. For a vector port, extract its .pins;
    for a single pin, return a one-element list. No connections are created.
    """

    # For a list/tuple, recursively unpack every item while preserving lane order.
    if isinstance(value, (tuple, list)):
        return [pin for item in value for pin in pins(item)]

    # A vector port supplies .pins; an individual pin becomes a one-item list.
    return list(value.pins) if hasattr(value, 'pins') else [value]


def join(left, right):
    """Connect equal-width bundles lane by lane, preserving their order.

    For example, left[0] connects to right[0]. Reject mismatched widths
    instead of silently leaving lanes unconnected.
    """
    left, right = pins(left), pins(right)
    if len(left) != len(right):
        raise ValueError(f'Connection width mismatch: {len(left)} != {len(right)}')
    for a, b in zip(left, right):
        connect(a, b)


def port(cell, name):
    """Retrieve cell terminals by their native library port name.

    Use the shared lookup so coordinate-adapted logical sides do not change
    which physical terminal the topology refers to.
    """
    return native_port(cell, name)


def gate_order(values):
    """Reverse two-lane group order while preserving order within each pair.

    For example, [0, 1, 2, 3, 4, 5] becomes [4, 5, 2, 3, 0, 1].
    This preserves the legacy selection-lane mapping; odd widths are invalid.
    """
    # Legacy correctPinOrder: reverse the two-lane groups, preserving pairs.
    values = pins(values)
    if len(values) % 2:
        raise ValueError('Shared gate selection requires two-lane groups')
    return [pin for i in range(len(values) - 2, -1, -2) for pin in values[i:i + 2]]


class CircuitBuilder:
    """Manage reusable construction operations for a single circuit.

    cells must already use process_coordinates. matrix_unit is the electrical
    capacity of one matrix cell, independent of its physical axis orientation.
    Supply aliases and automatically shared controls are explicit caller policy.
    See SYSTEM_BUILD_README.md for method contracts and examples.
    """

    def __init__(self, circuit, *, frame, cells, process_coordinates='xy',
                 matrix_unit=(4, 2), masters=None, supply_names=(),
                 supply_aliases=None, static_families=(), shared_controls=()):
        """Bind circuit/library objects and initialize separate per-design state."""
        self.circuit = circuit
        self.frame = frame
        self.cells = cells
        self.process_coordinates = process_coordinates
        self.rows_per_cell, self.cols_per_cell = matrix_unit
        if any(type(n) is not int or n < 1 for n in matrix_unit):
            raise ValueError('matrix_unit must contain two positive integers')
        self.profile = {'masters': dict(masters or {})}
        self.supply_aliases = dict(supply_aliases or {})
        self.static_families = frozenset(static_families)
        self.shared_controls = frozenset(shared_controls)
        self.islands, self.matrices, self.generated = {}, {}, {}
        self.support, self.exposed, self.controls, self.decoder_inputs = {}, {}, {}, {}
        self.supplies = {name: ac.Wire(circuit) for name in supply_names}

    def common(self, name, value):
        """Connect all supplied pins to one named shared supply or control net.

        Reuse a wire or create it on first use. Apply caller-selected supply aliases.
        Unlike join(), this ties all lanes together on the same net.
        """
        name = self.supply_aliases.get(name, name)
        pool = self.supplies if name in self.supplies else self.controls
        if name not in pool:
            pool[name] = ac.Wire(self.circuit)
        for pin in pins(value):
            connect(pin, pool[name])

    def expose(self, name, value, side='W'):
        """Create a frame port connected to the supplied internal pin lanes.

        Use side as the frame-side designation. Reusing a name joins the new
        lanes to the existing port; multiple lanes are packaged as a Bus.
        """
        values = pins(value)
        if not values:
            return

        # Reusing an external name connects to its existing lanes instead of adding a port.
        if name in self.exposed:
            join(self.exposed[name], values)
            return
        self.exposed[name] = values
        connection = values[0] if len(values) == 1 else ac.Bus(self.circuit, busElements=values)
        self.frame.createPort(side, name, dimension=len(values), connection=connection)

    def island(self, name):
        """Create and record a named placement group within the top circuit.

        The group owns instances for layout; it does not itself connect pins.
        """
        if name in self.islands:
            raise ValueError(f'Duplicate island name: {name}')
        value = ac.Island(self.circuit)
        self.islands[name] = value
        return value

    def static(self, cell):
        """Attach recognized supply and shared-control ports to common nets.

        Strip the final side suffix before matching, for example GND_w to GND.
        This includes changing controls such as RUN and PROG, not only DC rails.
        """
        for p in cell.ports:
            family = p.native_name.rsplit('_', 1)[0]
            if family in self.static_families:
                self.common(family, p)

    def bank(self, name, master, vertical, horizontal=1):
        """Create a support-cell array in its own named placement island.

        vertical and horizontal count physical instances. Resolve any profile
        master alias, place the array locally, and attach common supplies/controls.
        """
        owner = self.island(name)
        master = self.profile.get('masters', {}).get(master, master)
        grid = AlgorithmGrid.for_process(owner, self.process_coordinates)
        body = grid.create(getattr(self.cells, master), self.circuit, dim=(vertical, horizontal))
        grid.place(body, (0, 0))
        self.support[name] = body
        self.static(body)
        return body

    def register_fg(self, name, fg):
        """Record a generated programming-peripheral result and integrate its nets.

        Connect shared supplies and selected controls, then save available decoder
        input interfaces for the later low-voltage buffer wiring.
        """
        self.generated[name] = fg
        for key, value in fg.supplies.items():
            self.common(key, value)
        for key, value in fg.controls.items():
            if key in self.shared_controls:
                self.common(key, value)

        # Save decoder inputs for the low-voltage buffer connections built later.
        for role in ('gate', 'drain'):
            chain = getattr(fg, role)
            if chain is not None and chain.decoder_result is not None:
                self.decoder_inputs[(name, role)] = chain.inputs
        return fg

    def matrix(self, name, row_count, col_count, *, master='IndirectVMM_4x2', **options):
        """Create a matrix body and its requested local programming peripherals.

        row_count and col_count are electrical lane counts. Divide by the cell
        capacity to obtain the physical array dimensions. Forward options to the
        peripheral generator and return separate body and peripheral handles.
        """
        if (type(row_count) is not int or type(col_count) is not int
                or row_count < 1 or col_count < 1
                or row_count % self.rows_per_cell or col_count % self.cols_per_cell):
            raise ValueError('Matrix lanes must be positive whole multiples of matrix_unit')
        owner = self.island(name)
        master = self.profile.get('masters', {}).get(master, master)
        grid = AlgorithmGrid.for_process(owner, self.process_coordinates)
        # Golden XY dimensions are (rows, columns).
        body = grid.create(getattr(self.cells, master), self.circuit,
            dim=(row_count // self.rows_per_cell, col_count // self.cols_per_cell))
        grid.place(body, (0, 0))

        # Options select which programming blocks this matrix owns locally.
        fg = owner.generate_fg_peripherals(cells=self.cells, process_coordinates=self.process_coordinates, **options)
        self.matrices[name] = body
        self.register_fg(name, fg)

        # Return separate handles for the matrix body and its programming interfaces.
        return body, fg

    def drain_extension(self, name, bodies, program_only=()):
        """Generate a separate drain peripheral group for the supplied bodies.

        Regular bodies provide programming and read drain ports. program_only
        bodies provide programming ports with no read interface in this group.
        Register the result so shared rails and decoder inputs are integrated.
        """
        fg = generate_drain_extension(self.island(name),
            [(port(body, 'Vd_P_n'), port(body, 'Vd_R_n')) for body in bodies]
            + [(port(body, 'Vd_P_n'), None) for body in program_only],
            cells=self.cells, process_coordinates=self.process_coordinates)
        return self.register_fg(name, fg)

