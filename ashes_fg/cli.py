#!/usr/bin/env python3

# CLI, Command Line Invocation, for calling the ashes toolchain
# Requires command line argument for FPAA vs ASIC compilation
# Usage: ashes asic design.py or ashes fpaa design.py


def main():
    import argparse
    import json
    from pathlib import Path
    import ashes_fg as af


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

   # ---- load design ----
    globals_dict = {}
    with open(design_path) as f:
        exec(f.read(), globals_dict)

    if "Top" not in globals_dict:
        raise SystemExit("Algorithm must define `Top` Circuit object")

    design = globals_dict["Top"]

    # ---- load config ----
    config_path = project_dir / "ashes.json"
    compile_args = {}
    if config_path.exists():
        with open(config_path) as f:
            compile_args = json.load(f)

    # ---- dispatch ----
    if args.flow == "fpaa":
        af.fpaa.compile(design, **compile_args)
    elif args.flow == "asic":
        af.asic.compile(design,process="tsmc_350nm",fileName="LPFMeadSOS")

if __name__ == "__main__":
    main()
