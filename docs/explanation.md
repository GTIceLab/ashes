# Explanations

## High-level Code Overview
FPAA programming steps:

1. Python $\rightarrow$ Verilog (`new_converter.py`)
    - We want to replace with `asic_compile.py` in the future.
2. Verilog $\rightarrow$ Blif (`verilog2blif.py`)
3. Generate pad information (`gen_pads.30a.py`)
4. Blif $\rightarrow$ Switchlist (`blif_to_switches.py`)
    - Runs placement (VPR)
    - Generates switchlist
5. Switchlist $\rightarrow$ Assembly (`Make_ProgramList_CompileAssembly`)
6. Programm FPAA (`program_fpaa.py`)

Many scripts call lower-level functions from `rasp30`, such as
- TCL scripts for programming MSP430
- Architecture scripts that describe FPAA for VPR