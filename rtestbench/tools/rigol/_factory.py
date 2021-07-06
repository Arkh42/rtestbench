"""Factory functions for all rigol instruments."""


from rtestbench.tools.rigol.oscilloscope import ds1102


def get_rigol_tool(tool_info):
    """Returns the dedicated rigol Tool based on the model.
    
    Raises:
        ValueError: The model is not known from the system.
    """

    try:
        return get_rigol_oscilloscope(tool_info)
    except ValueError: # When other families are added, update this part of the code.
        raise ValueError("Unknown rigol family of instruments/tools.")


def get_rigol_oscilloscope(tool_info):
    # DS1102x series
    if tool_info.model == "DS1102E":
        return ds1102.DS1102E(tool_info)
    else:
        raise ValueError("Unknown rigol electrometer model")
