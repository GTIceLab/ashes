"""Central physical-design tool definitions.

External tools share conventional Verilog, macro LEF/DEF preparation, IO
margins, and per-tool folders. Register new tools here and implement their
_<tcl_prefix>_<step> functions in pd_tcl_gen.py. A compatible tool can reuse
an existing prefix. ASHES chooses its detailed router independently.
"""

PD_TOOLS = {
    "ashes": {"external": False, "tcl_prefix": None},
    "cadence": {"external": True, "tcl_prefix": "cadence"},
    "openroad": {"external": True, "tcl_prefix": "openroad"},
}


def get_pd_tool(pd_tool):
    if not isinstance(pd_tool, str) or pd_tool not in PD_TOOLS:
        choices = ", ".join(repr(name) for name in PD_TOOLS)
        raise ValueError(f"Select pd_tool from: {choices}.")
    return PD_TOOLS[pd_tool]


def is_external_pd_tool(pd_tool):
    return get_pd_tool(pd_tool)["external"]
