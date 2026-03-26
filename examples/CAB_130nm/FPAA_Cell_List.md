## Cells needed for FPAA

- Cab devices (Symbols for these Cells doesnt need to tile/abut)
    - sky130_cells/TA_FGbias_1x2 (Done)
    - sky130_cells/Cap_Bank (Done)
    - sky130_cells/FETs/alexpmos (Someone needs to verify this)
    - sky130_cells/TGate_2nMirror (Done)

- Symbols need to Abut for these
    - sky130_cells/IndirectVMM_GSwcs_1x2  (Eugene needs to push his update) 
        - Should abut with IndirectVMM_4x2 veritcally (Sits on top of IndirectVMM_4x2)
    - sky130_cells/IndirectVMM_4x2
        - Should abut with itself in both direction
    - sky130_cells/Tgates_Cutoff_Drlines
        - This cell is part of Drainswcs, someone needs to create a cell for this. (350nm_cells/Indirect_DrainSwcs/Symbols/TSMC350nm_4TGate_ST_draincutoff.png)
        - Should abut with IndirectVMM_4x2 horizontally (Sits adjacent to the side of IndirectVMM_4x2)
    - sky130_cells/IndirectVMM_DrainSwcs (Will needs to push his update) 
        - Should abut with IndirectVMM_4x2 horizontally (Sits adjacent to the side of IndirectVMM_4x2)
    - sky130_cells/Level_Shifter/Horizontal_LS 
        - Should abut with IndirectVMM_DrainSwcs horizontally
    - sky130_cells/Level_Shifter/Vertical_LS
        - Should abut with IndirectVMM_GSwcs vertically
    - sky130_cells/Voltaile_Swcs (Will needs to push his update) 
        - Should abut with itself in horizontal direction
    - sky130_cells/IndirectVMM_Bot_Bmat_4x2
        - Abut with itself in Horizontal direction
        - Use the symbol created for IndirectVMM_4x2 and tweak it        
    - sky130_cells/IndirectVMM_Top_AorBmat_4x2
        - Abut with itself in Horizontal direction
        - Use the symbol created for IndirectVMM_4x2 and tweak it
    - sky130_cells/IndirectVMM_GSwcs_1x2
        - Sits anove and abuts with IndirectVMM_Top_AorBmat_4x2
    - sky130_cells/IndirctGswc_OutMat
        - Sits below and abuts with IndirectVMM_Bot_Bmat_4x2

- Decoders need to be made