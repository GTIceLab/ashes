"""Build the programming and run-mode assembly for a RASP 3.0 project.

Refactor of the Python port of MakeProgramlilst_CompileAssembly.sce.

Public API (unchanged):
    compile(project_name, board_type, chip_num)       -> None
    diodeADC_v2i / _i2v / _v2h / _h2v(value, chip_num, brdtype)
    mismatch_map_compensation(target_list, chip_num, brdtype, path, switch_list_ble)
    KAPPA_CONSTANT, ASHESPATH, RASPPATH

Everything is read from / written to ``$ASHESPATH/<project_name>`` (``path``);
the tool chain lives under ``$RASPPATH/prog_assembly/libs``.  Nothing depends on the
current working directory.  ``path/hid_dir`` receives the assembler by-products.

Columns of a .swcs row (always exactly four):
    row, col, value, kind
where ``kind`` is 0 for a plain switch (``value`` is then the switch state, 2 = BLE),
and otherwise (``value`` is a target current in amps):
    1 switch FG, 2 OTA_ref FG (bias), 3 OTA FG, 4 MITE, 5 BLE, 6 direct SWC FG,
    11..15 = same as 1..5 but also listed in the mismatch calibration list.
"""
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np

KAPPA_CONSTANT = 30  # relationship of target current between subVt and lowsubVt range.
ASHESPATH = os.getenv("ASHESPATH", "/home/ubuntu/ashes")
RASPPATH = os.getenv("RASPPATH", "/home/ubuntu/rasp30")

VDD = 2.5
THERMAL_VOLTAGE = 0.0258  # kT/q used by the diode-ADC EKV model

_BOARD_SUFFIX = {"3.0": "", "3.0a": "_30a", "3.0n": "_30n", "3.0h": "_30h"}
_MEMORY_ARGS = ("16384", "16384", "16384")  # prog / data / peripheral sizes for asm2ihex2.sh
_CHIP_PARA = ("TR", "SP", "RI", "CP", "FP")

# Boundaries between the programming current ranges (amps).
_HIGH_ABOVE_VT_MIN = 10e-6
_ABOVE_VT_MIN = 1e-7
_SUB_VT_MIN = 1e-9
# Switch rows carry no target current; programming them with 0 caused errors.
_SWITCH_PLACEHOLDER_CURRENT = 100e-9


def _libs():
    return Path(RASPPATH) / "prog_assembly" / "libs"


# --------------------------------------------------------------------------- #
# Diode ADC model (EKV).  Parameter file: Is, VT, kappa, Slope_v2h, Offset_v2h
# --------------------------------------------------------------------------- #

def _ekv_params(chip_num, brdtype):
    param_file = _libs() / "chip_parameters" / "EKV_diodeADC" / f"EKV_diodeADC_chip{chip_num}{brdtype}"
    Is, VT, kappa, slope_v2h, offset_v2h = np.loadtxt(param_file, delimiter=",")[:5]
    return Is, VT, kappa, slope_v2h, offset_v2h


def diodeADC_v2i(Vfg, chip_num, brdtype):
    Is, VT, kappa, _, _ = _ekv_params(chip_num, brdtype)
    return Is * np.power(np.log(1 + np.exp(kappa * ((VDD - Vfg) - VT) / (2 * THERMAL_VOLTAGE))), 2)


def diodeADC_i2v(Isat, chip_num, brdtype):
    Is, VT, kappa, _, _ = _ekv_params(chip_num, brdtype)
    return VDD - ((np.log(np.exp(np.sqrt(Isat / Is)) - 1) * (2 * THERMAL_VOLTAGE) / kappa) + VT)


def diodeADC_v2h(Vfg, chip_num, brdtype):
    _, _, _, slope_v2h, offset_v2h = _ekv_params(chip_num, brdtype)
    return slope_v2h * 2 * (VDD - Vfg) + offset_v2h


def diodeADC_h2v(hex, chip_num, brdtype):
    _, _, _, slope_v2h, offset_v2h = _ekv_params(chip_num, brdtype)
    return VDD - ((hex - offset_v2h) / slope_v2h) / 2


# --------------------------------------------------------------------------- #
# Small file / process helpers
# --------------------------------------------------------------------------- #

def _hex(value):
    """16-bit hex word as the firmware expects it, e.g. ``0x00ff`` (truncates fractions)."""
    word = int(value)
    if not 0 <= word <= 0xFFFF:
        raise ValueError(f"value {value!r} does not fit in a 16-bit word")
    return f"0x{word:04x}"


def _write_text(path, text):
    Path(path).write_text(text + "\n")


def _save_matrix(path, matrix):
    np.savetxt(str(path), matrix, fmt="%5.15f", delimiter=" ")


def _run_asm2ihex(name, source, path):
    """Assemble ``source`` into ``path/<name>.elf`` (plus .o/.l43/pmem.x/pmem_defs.asm)."""
    script = _libs() / "sh" / "asm2ihex2.sh"
    # asm2ihex2.sh reads $RASPPATH itself, so hand it the value this module uses.
    env = dict(os.environ, RASPPATH=str(RASPPATH))
    subprocess.run([str(script), name, str(source), *_MEMORY_ARGS, str(path)], check=True, env=env)


def _copy(src, dst):
    Path(dst).write_bytes(Path(src).read_bytes())


def _move_into(src, directory):
    os.replace(src, Path(directory) / Path(src).name)  # like `mv`: overwrites


# --------------------------------------------------------------------------- #
# Project context
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class _Project:
    name: str
    path: Path
    hid_dir: Path
    chip_num: str
    brdtype: str

    def chip_file(self, subdir, stem, ext=""):
        return _libs() / "chip_parameters" / subdir / f"{stem}_chip{self.chip_num}{self.brdtype}{ext}"


def _board_suffix(board_type):
    try:
        return _BOARD_SUFFIX[board_type]
    except KeyError:
        raise ValueError(
            f"Please select the FPAA board that you are using (got {board_type!r}; "
            f"expected one of {sorted(_BOARD_SUFFIX)})"
        ) from None


def _stage_chip_files(project):
    """Copy the chip-specific parameter files into the project directory."""
    para_dir = _libs() / "chip_parameters" / "chip_para"
    _copy(para_dir / "chip_para_debug.asm", project.path / "chip_para_debug.asm")
    for tag in _CHIP_PARA:
        _copy(project.chip_file("chip_para", f"chip_para_{tag}", ".asm"), project.path / f"chip_para_{tag}.asm")
    _copy(project.chip_file("Vd_table", "Vd_table_30mV"), project.path / "Vd_table_30mV")


def _load_swcs(path, project_name):
    swcs = np.loadtxt(f"{path}/{project_name}.swcs", ndmin=2)
    if swcs.size == 0:
        raise ValueError(f"{project_name}.swcs is empty")
    if swcs.shape[1] != 4:
        raise ValueError(f"{project_name}.swcs: expected 4 columns, found {swcs.shape[1]}")
    return swcs


# --------------------------------------------------------------------------- #
# Switch programs
# --------------------------------------------------------------------------- #

def _switch_info_text(switches, ble_state_as_zero=True):
    """Hex image uploaded to SRAM: count, then (row, col, state) per switch.

    ``switch_info`` stores BLE switches (state 2) as 0; ``switch_info_ble`` keeps the 2.
    """
    text = f"{_hex(len(switches))} "
    for row, col, state in switches:
        if ble_state_as_zero and state == 2:
            state = 0
        text += f"{_hex(row)} {_hex(col)} {_hex(state)} "
    return text


def _build_switch_programs(swcs, project):
    path, asm = project.path, _libs() / "asm_code"

    switches = swcs[swcs[:, 3] == 0, :3]
    if len(switches) == 0:
        raise ValueError(f"{project.name}.swcs contains no switches")
    _save_matrix(path / "switch_list", switches)
    _write_text(path / "switch_info", _switch_info_text(switches))
    _run_asm2ihex("switch_program", asm / "switch_program_ver04.s43", path)

    # BLE switches: state 2.  Stale copies from a previous run are removed first.
    for stale in ("switch_list_ble", "switch_info_ble"):
        try:
            (project.hid_dir / stale).unlink()
        except FileNotFoundError:
            pass
    ble = switches[switches[:, 2] == 2]
    if len(ble):
        _save_matrix(path / "switch_list_ble", ble)
        _write_text(path / "switch_info_ble", _switch_info_text(ble, ble_state_as_zero=False))
        _run_asm2ihex("tunnel_clb", asm / "tunnel_revtun_CLB_ver00.s43", path)
        _run_asm2ihex("switch_program_ble", asm / "switch_program_ble_ver00.s43", path)
        _move_into(path / "switch_list_ble", project.hid_dir)
        _move_into(path / "switch_info_ble", project.hid_dir)


# --------------------------------------------------------------------------- #
# Target preparation: mismatch map, calibration list, kappa scaling, ADC code
# --------------------------------------------------------------------------- #

def _apply_mismatch_map(targets, chip_num, brdtype, path):
    """Shift each non-switch target by the chip's mismatch map (in place)."""
    map_file = _libs() / "chip_parameters" / "mismatch_map" / f"mismatch_map_chip{chip_num}{brdtype}"
    if not map_file.exists():
        return
    mismatch = np.loadtxt(map_file, delimiter=",", ndmin=2)
    if mismatch.size:
        for i in np.flatnonzero(targets[:, 3] != 0):
            same_cell = (mismatch[:, 0] == targets[i, 0]) & (mismatch[:, 1] == targets[i, 1])
            for offset in mismatch[same_cell, 2]:  # every match applies, in map order
                targets[i, 2] = diodeADC_v2i(diodeADC_i2v(targets[i, 2], chip_num, brdtype) + offset, chip_num, brdtype)
    _save_matrix(Path(path) / "mismatch_mapped_swc_list", targets)


def _extract_calibration_rows(targets, path):
    """Save rows of kind 11..15 as the calibration list and turn them into kind 1..5 (in place)."""
    is_cal = np.isin(targets[:, 3], (11, 12, 13, 14, 15))
    if is_cal.any():
        _save_matrix(Path(path) / "mismatch_calibration_list", targets[is_cal])
        targets[is_cal, 3] -= 10


def _kappa_scaled_currents(targets):
    """Currents moved into the range the diode ADC can measure (subVt <-> lowsubVt)."""
    current = targets[:, 2]
    current = np.where(current < _SUB_VT_MIN, current * KAPPA_CONSTANT, current)
    return np.where(current > _HIGH_ABOVE_VT_MIN, current / KAPPA_CONSTANT, current)


def _prepare_targets(swcs, chip_num, brdtype, path):
    """Return an (n, 5) array: row, col, current, kind, ADC code (kind 11..15 already folded to 1..5)."""
    targets = swcs.copy()
    targets[targets[:, 3] == 0, 2] = _SWITCH_PLACEHOLDER_CURRENT
    _apply_mismatch_map(targets, chip_num, brdtype, path)
    _extract_calibration_rows(targets, path)
    scaled = _kappa_scaled_currents(targets)
    codes = diodeADC_v2h(diodeADC_i2v(scaled, chip_num, brdtype), chip_num, brdtype)
    return np.column_stack([targets, codes])


def mismatch_map_compensation(target_list, chip_num, brdtype, path, switch_list_ble=None):
    """Compatibility wrapper for the old helper.

    Mutates ``target_list`` in place (compensated current, calibration kinds folded) and returns a
    copy whose current column is kappa-scaled.  ``switch_list_ble`` is ignored (it was only ever
    written to the wrong output file).
    """
    targets = np.asarray(target_list, dtype=float)
    _apply_mismatch_map(targets, chip_num, brdtype, path)
    _extract_calibration_rows(targets, path)
    scaled = targets.copy()
    scaled[:, 2] = _kappa_scaled_currents(targets)
    return scaled


# --------------------------------------------------------------------------- #
# Target programs.  One "group" = one device class in one current range.
# --------------------------------------------------------------------------- #

_RANGES = ("highaboveVt", "aboveVt", "subVt", "lowsubVt")
_DEVICES = ("swc", "ota", "otaref", "mite", "dirswc")
_HAS_HIGH_RANGE = ("swc", "ota")
_KIND_TO_DEVICE = {1: "swc", 5: "swc", 3: "ota", 2: "otaref", 4: "mite", 6: "dirswc"}
_ASM_SUFFIX = {"swc": "SWC", "ota": "CAB_ota", "otaref": "CAB_ota_ref", "mite": "CAB_mite", "dirswc": "DIRSWC"}


@dataclass(frozen=True)
class _Group:
    current_range: str
    device: str

    @property
    def name(self):
        return f"{self.current_range}_{self.device}"

    @property
    def pulse_table(self):
        if self.current_range == "lowsubVt":
            return f"pulse_width_table_lowsubVt_{self.device}"
        return f"pulse_width_table_{self.device}"

    def asm_steps(self):
        """(output name, source .s43) for recover_inject, first/measured coarse and fine programs."""
        rng, sfx = self.current_range, _ASM_SUFFIX[self.device]
        # recover_inject / first_coarse_program are shared by aboveVt and subVt, so their sources
        # carry no range in the file name.
        shared = sfx if rng in ("aboveVt", "subVt") else f"{rng}_{sfx}"
        return [
            (f"recover_inject_{rng}_{sfx}", f"recover_inject_{shared}.s43"),
            (f"first_coarse_program_{rng}_{sfx}", f"first_coarse_program_{shared}.s43"),
            (f"measured_coarse_program_{rng}_{sfx}", f"measured_coarse_program_{rng}_{sfx}.s43"),
            (f"fine_program_{rng}_m_ave_04_{sfx}", f"fine_program_{rng}_m_ave_04_{sfx}.s43"),
        ]


def _valid(rng, device):
    return rng != "highaboveVt" or device in _HAS_HIGH_RANGE


# Order the programs are built in, and order of the counts in the ``target_list`` file.
_BUILD_ORDER = tuple(_Group(r, d) for d in _DEVICES for r in _RANGES if _valid(r, d))
_INFO_ORDER = tuple(_Group(r, d) for r in _RANGES for d in _DEVICES if _valid(r, d))


def _current_range(current, device):
    if device in _HAS_HIGH_RANGE and current > _HIGH_ABOVE_VT_MIN:
        return "highaboveVt"
    if current > _ABOVE_VT_MIN:
        return "aboveVt"
    if current >= _SUB_VT_MIN:
        return "subVt"
    return "lowsubVt"


def _target_info_text(rows):
    """Count, then per target: row, col, ADC code, diff (0x0000), # of pulses (0xffff = not started)."""
    text = f"{_hex(len(rows))} "
    for row, col, code in rows:
        text += f"{_hex(row)} {_hex(col)} {_hex(code)} 0x0000 0xffff "
    return text


def _build_group(group, rows, project):
    path, asm = project.path, _libs() / "asm_code"
    table = group.pulse_table
    _copy(project.chip_file("pulse_width_table", table), path / table)
    _save_matrix(path / f"target_list_{group.name}", rows[:, :3])
    _write_text(path / f"target_info_{group.name}", _target_info_text(rows[:, [0, 1, 3]]))
    for name, source in group.asm_steps():
        _run_asm2ihex(name, asm / source, path)


def _build_target_programs(targets, project):
    path = project.path
    groups = {group: [] for group in _BUILD_ORDER}
    tunnel_rows = []
    for row, col, current, kind, code in targets[targets[:, 3] != 0]:
        tunnel_rows.append((row, col, code))
        device = _KIND_TO_DEVICE.get(kind)
        if device is not None:
            groups[_Group(_current_range(current, device), device)].append((row, col, current, code))

    counts = [len(tunnel_rows)] + [len(groups[g]) for g in _INFO_ORDER] + [KAPPA_CONSTANT]
    _save_matrix(path / "target_list", counts)

    if tunnel_rows:
        _write_text(path / "target_info_tunnel_revtun", _target_info_text(tunnel_rows))
    for group in _BUILD_ORDER:
        if groups[group]:
            _build_group(group, np.array(groups[group]), project)


# --------------------------------------------------------------------------- #
# Run mode
# --------------------------------------------------------------------------- #

@dataclass
class RunModeFlags:
    """Run-mode selectors.

    In the Scilab tool these were ``global`` variables filled in by other scripts of the GUI flow.
    For a .swcs project they are all forced to 0, which is the only case ``compile`` runs today.
    """
    ramp_adc: int = 0
    sftreg: int = 0
    signal_dac: int = 0
    gpio_in: int = 0
    mite_adc: int = 0
    onchip_adc: int = 0
    counter: int = 0


def _voltage_meas_sources(flags, swcs_input):
    """Sources to assemble as ``voltage_meas``, in order (a later build overwrites an earlier one)."""
    sources = []
    if swcs_input:
        flags = RunModeFlags()
        sources.append("voltage_measurement_ver01_withoutMITE.s43")
    sig, gpio, mite, ramp = flags.signal_dac == 1, flags.gpio_in, flags.mite_adc, flags.ramp_adc
    if sig and gpio == 0 and mite == 0:
        sources.append("voltage_measurement_ver01_withoutMITE.s43")
    if sig and gpio == 0 and mite == 1:
        sources.append("voltage_measurement_ver01_withMITE.s43")
    if sig and gpio == 1 and mite == 1:
        sources.append("runmode_signalDAC_gpin_miteADC.s43")
    if sig and gpio == 0 and ramp == 1:
        sources.append("sftreg_adc.s43" if flags.sftreg == 1 else "Ramp_ADC_DAC.s43")
    if sig and gpio == 1 and ramp == 1:
        sources.append("runmode_signalDAC_gpin_rampADC.s43")
    if sig and flags.onchip_adc == 1:
        sources.append("ADC_onchip.s43")
    if sig and flags.counter == 1:
        sources.append("Counter.s43")
    return sources


def _write_output_info(targets, path):
    """List the MITE targets whose outputs are read back in run mode; returns how many."""
    mites = targets[targets[:, 3] == 4]
    text = f"{_hex(len(mites))} " + "".join(f"{_hex(row)} {_hex(col)} " for row, col in mites[:, :2])
    _write_text(Path(path) / "output_info", text)
    return len(mites)


def _input_vector_is_idle(path):
    """True if row 1, column 2 of ``input_vector`` is zero (decimal or hex)."""
    with open(Path(path) / "input_vector") as handle:
        for line in handle:
            fields = line.split()
            if fields and not fields[0].startswith("#"):
                break
        else:
            raise ValueError("input_vector is empty")
    if len(fields) < 2:
        raise ValueError("input_vector: first row needs at least two columns")
    try:
        return float(fields[1]) == 0
    except ValueError:
        return int(fields[1], 16) == 0


def _build_run_mode_programs(n_mite, path):
    asm = _libs() / "asm_code"
    _run_asm2ihex("run_mode_after_program", asm / "voltage_measurement_ver01_afterprogram.s43", path)

    flags = RunModeFlags()
    if n_mite:
        flags.mite_adc = 1
    for source in _voltage_meas_sources(flags, swcs_input=True):
        _run_asm2ihex("voltage_meas", asm / source, path)

    if _input_vector_is_idle(path):
        _run_asm2ihex("voltage_meas", asm / "voltage_measurement_ver01_just_runmode.s43", path)


def _archive_intermediates(project):
    """Move assembler by-products and the staged chip_para files into hid_dir."""
    names = ["chip_para_debug.asm"] + [f"chip_para_{tag}.asm" for tag in _CHIP_PARA] + ["pmem.x", "pmem_defs.asm"]
    candidates = [project.path / n for n in names]
    candidates += sorted(project.path.glob("*.l43")) + sorted(project.path.glob("*.o"))
    for candidate in candidates:
        if candidate.exists():
            _move_into(candidate, project.hid_dir)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def compile(project_name, board_type, chip_num):
    brdtype = _board_suffix(board_type)
    path = Path(f"{ASHESPATH}/") / project_name
    hid_dir = path / "hid_dir"
    hid_dir.mkdir(exist_ok=True)
    project = _Project(project_name, path, hid_dir, chip_num, brdtype)

    _stage_chip_files(project)

    # Program / reverse-tunnel program (executed later by program_fpaa.py)
    _run_asm2ihex("tunnel_revtun_SWC_CAB", _libs() / "asm_code" / "tunnel_revtun_SWC_CAB_ver00.s43", path)

    swcs = _load_swcs(path, project_name)
    _build_switch_programs(swcs, project)
    targets = _prepare_targets(swcs, chip_num, brdtype, path)
    _build_target_programs(targets, project)

    n_mite = _write_output_info(targets, path)
    _build_run_mode_programs(n_mite, path)
    _archive_intermediates(project)
