grid 0.05um 0.05um
snap user
load "../../../ASHES-Skywater130nm/sky130_cells/G_or_S_IndrctSwcs/G_or_S_IndrctSwcs.mag"
gds write "../../examples/mag2stdcells/G_or_S_IndrctSwcs.gds"
quit -noprompt
