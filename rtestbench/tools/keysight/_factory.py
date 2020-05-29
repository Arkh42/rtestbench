"""Factory functions for all Keysight instruments."""


from rtestbench.tools.keysight.electrometer import b298x


def get_keysight_tool(tool_info):
    """Returns the dedicated Keysight Tool based on the model.
    
    Raises:
        ValueError: The model is not known from the system.
    """

    if tool_info.family == "electrometer":
        return get_keysight_electrometer(tool_info)
    else:
        raise ValueError("Unknow Keysight family of instruments/tools.")


def get_keysight_electrometer(tool_info):
    # B298X series
    if tool_info.model == "B2981A":
        return b298x.B2981(tool_info)
    elif tool_info.model == "B2983A":
        return b298x.B2983(tool_info)
    elif tool_info.model == "B2985A":
        return b298x.B2985(tool_info)
    elif tool_info.model == "B2987A":
        return b298x.B2987(tool_info)
    else:
        raise ValueError("Unknown Keysight electrometer model")
