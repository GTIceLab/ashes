#!/usr/bin/env python3

# CLI, Command Line Invocation, for calling the ashes toolchain
# Requires command line argument for FPAA vs ASIC compilation
# Usage: ashes asic design.py or ashes fpaa design.py


def main():
    import argparse
    import json
    from pathlib import Path
    import ashes_fg as af
    import os
    import sys


    parser = argparse.ArgumentParser(prog="ashes")
    # Require user to specify fpaa or asic
    subparsers = parser.add_subparsers(dest="flow", required=True)

    # -------- FPAA --------
    fpaa = subparsers.add_parser("fpaa", help="FPAA compile flow")
    fpaa.add_argument("design", help="Design file")

    # -------- ASIC --------
    asic = subparsers.add_parser("asic", help="ASIC compile flow")
    asic.add_argument("design", help="Design file")

    args = parser.parse_args()

    design_path = Path(args.design).resolve()
    project_dir = design_path.parent

    # Make local imports work
    sys.path.insert(0, str(project_dir))

    # ---- load design ----
    globals_dict = {}
    with open(design_path) as f:
        code = compile(f.read(), design_path, "exec")
        exec(code, globals_dict)

    # Remove local modules from path
    sys.path.pop(0)

    if "Top" not in globals_dict:
        raise SystemExit("Algorithm must define `Top` Circuit object")

    # Variables from design
    design = globals_dict["Top"]
    design_limits = globals_dict["design_limits"]
    location_islands = globals_dict["location_islands"]


    # ---- load synthesis settings ----
    config_path = project_dir / "synthesis_settings.json"
    compile_args = {}
    if config_path.exists():
        with open(config_path) as f:
            compile_args = json.load(f)
    

    # ---- load routing settings ----
    config_path = project_dir / "router_settings.json"
    qparams = {}
    if config_path.exists():
        with open(config_path) as f:
            qparams = json.load(f)
    else:
        qparams = None


    # ---- load synthesis settings ----
    config_path = project_dir / "pd_cadence_settings.json"
    pd_args = {}
    if config_path.exists():
        with open(config_path) as f:
            pd_args = json.load(f)
            
            
    # Assume project name is folder name
    project_name = Path(args.design).stem

    # ---- dispatch ----
    if args.flow == "fpaa":
        af.fpaa.compile(design, **compile_args)
    elif args.flow == "asic":
        af.asic.compile(design,project_path = project_dir,project_name=project_name,design_limits=design_limits,location_islands=location_islands,qparams=qparams,pd_args=pd_args,**compile_args)

if __name__ == "__main__":
    main()
