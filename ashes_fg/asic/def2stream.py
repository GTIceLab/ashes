try:
    import pya
except ImportError:
    pya = None

import re
import sys
import os


def merge_gds(
    pya_mod,
    tech_file,
    layer_map,
    in_def,
    design_name,
    in_files,
    seal_file,
    out_file,
    allow_empty="",
    tech_lef="",
    macro_lefs="",
    def_units=1000,
):
    """Merge DEF and GDS/OAS files into a single stream file.

    Args:
        pya_mod: The pya module (klayout Python API).
        tech_file: Path to KLayout technology file; empty when using tech_lef.
        layer_map: Path to layer map file (empty string if none).
        in_def: Path to input DEF file.
        design_name: Top-level design name.
        in_files: Space-separated string of GDS/OAS files to merge.
        seal_file: Path to seal ring GDS/OAS file (empty string if none).
        out_file: Path to output GDS/OAS file.
        allow_empty: Regex pattern for cells allowed to be empty.
        tech_lef: External technology LEF instead of a .lyt (requires layer_map).
        macro_lefs: Optional semicolon-separated additional cell/macro LEF paths.
        def_units: Reader units per micron (default 1000); does not override DEF header units.

    Returns:
        Number of errors encountered.
    """
    try:
        def_units = int(str(def_units))
        if def_units <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("def_units must be a positive integer, e.g. 1000 or 2000") from None
    reader_dbu = 1.0 / def_units
    errors = 0

    # Use either a saved technology or external LEFs directly.
    if bool(tech_file) == bool(tech_lef):
        raise ValueError("Supply exactly one of -rd tech_file=... or -rd tech_lef=...")
    if tech_file:
        tech = pya_mod.Technology()
        tech.load(tech_file)
        layout_options = tech.load_layout_options
    else:
        if not layer_map:
            raise ValueError("Direct tech_lef mode requires -rd layer_map=...")
        layout_options = pya_mod.LoadLayoutOptions()

    config = layout_options.lefdef_config
    config.dbu = reader_dbu
    if tech_lef:
        config.lef_files = [tech_lef]
    extra_lefs = [path.strip() for path in macro_lefs.split(";") if path.strip()]
    if extra_lefs:
        config.lef_files = list(config.lef_files) + extra_lefs
    if layer_map:
        config.map_file = layer_map
    layout_options.lefdef_config = config
    print(f"[INFO] Reader units: {def_units}/micron (DBU={reader_dbu} microns)", flush=True)

    # Load def file
    main_layout = pya_mod.Layout()
    print("[INFO] Reporting cells prior to loading DEF ...")
    for i in main_layout.each_cell():
        print("[INFO] '{0}'".format(i.name))

    main_layout.read(in_def, layout_options)

    # Clear cells
    top_cell_index = main_layout.cell(design_name).cell_index()

    # remove orphan cell BUT preserve cell with VIA_
    #  - KLayout is prepending VIA_ when reading DEF that instantiates LEF's via
    for i in main_layout.each_cell():
        if i.cell_index() != top_cell_index:
            if not i.name.startswith("VIA_") and not i.name.endswith("_DEF_FILL"):
                i.clear()

    # Load in the gds to merge
    for fil in in_files.split():
        print("\t{0}".format(fil))
        expected_dbu = main_layout.dbu
        main_layout.read(fil)
        if abs(main_layout.dbu - expected_dbu) > 1e-12:
            raise ValueError(
                f"GDS DBU mismatch in {fil}: reader DBU={expected_dbu}, "
                f"GDS DBU={main_layout.dbu}. Stopping before output to prevent "
                "incorrect placement scaling. Use compatible reader/GDS units "
                "or a DBU-aware merge."
            )

    # Copy the top level only to a new layout
    top_only_layout = pya_mod.Layout()
    top_only_layout.dbu = main_layout.dbu
    top = top_only_layout.create_cell(design_name)
    top.copy_tree(main_layout.cell(design_name))

    missing_cell = False
    regex = re.compile(allow_empty) if allow_empty else None

    if allow_empty:
        print(f"[INFO] GDS_ALLOW_EMPTY={allow_empty}")

    for i in top_only_layout.each_cell():
        if i.is_empty():
            missing_cell = True
            if regex is not None and regex.match(i.name):
                print(
                    "[WARNING] LEF Cell '{0}' ignored. Matches GDS_ALLOW_EMPTY.".format(
                        i.name
                    )
                )
            else:
                print(
                    "[ERROR] LEF Cell '{0}' has no matching GDS/OAS cell."
                    " Cell will be empty.".format(i.name)
                )
                errors += 1

    if not missing_cell:
        print("[INFO] All LEF cells have matching GDS/OAS cells")

    orphan_cell = False
    for i in top_only_layout.each_cell():
        if i.name != design_name and i.parent_cells() == 0:
            orphan_cell = True
            print("[ERROR] Found orphan cell '{0}'".format(i.name))
            errors += 1

    if not orphan_cell:
        print("[INFO] No orphan cells in the final layout")

    if seal_file:
        top_cell = top_only_layout.top_cell()

        expected_dbu = top_only_layout.dbu
        top_only_layout.read(seal_file)
        if abs(top_only_layout.dbu - expected_dbu) > 1e-12:
            raise ValueError("Seal-ring GDS DBU mismatch; stopping before output to prevent incorrect scaling.")

        for cell in top_only_layout.top_cells():
            if cell != top_cell:
                print(
                    "[INFO] Merging '{0}' as child of '{1}'".format(
                        cell.name, top_cell.name
                    )
                )
                top.insert(pya_mod.CellInstArray(cell.cell_index(), pya_mod.Trans()))

    # Write out the GDS
    top_only_layout.write(out_file)

    return errors


# KLayout injects -rd arguments as globals.
if pya is not None:
    print("[INFO] def2stream started", flush=True)
    required = ("in_def", "design_name", "in_files", "out_file")
    missing = [name for name in required if not globals().get(name)]
    if missing:
        print("[ERROR] Missing -rd arguments: " + ", ".join(missing), file=sys.stderr, flush=True)
        sys.exit(2)
    try:
        result = merge_gds(
            pya_mod=pya,
            tech_file=globals().get("tech_file", ""),
            layer_map=globals().get("layer_map", ""),
            in_def=in_def,
            design_name=design_name,
            in_files=in_files,
            seal_file=globals().get("seal_file", ""),
            out_file=out_file,
            allow_empty=os.environ.get("GDS_ALLOW_EMPTY", ""),
            tech_lef=globals().get("tech_lef", ""),
            macro_lefs=globals().get("macro_lefs", ""),
            def_units=globals().get("def_units", 1000),
        )
    except Exception:
        import traceback
        traceback.print_exc()
        sys.stderr.flush()
        sys.exit(1)
    print(f"[INFO] def2stream finished with {result} error(s)", flush=True)
    sys.exit(result)
