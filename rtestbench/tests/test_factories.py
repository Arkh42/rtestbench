"""Test of all dedicated factories."""


import pytest

from rtestbench.core import ToolInfo
from rtestbench.tools.keysight import _factory as keysight_factory
from rtestbench.tools.keysight.electrometer import b298x


@pytest.fixture
def info_unknown():
    tool_info = ToolInfo()

    tool_info.family = "unknown"
    tool_info.model = "unknown"

    return tool_info

@pytest.fixture
def info_keysight_b2891():
    tool_info = ToolInfo()

    tool_info.family = "electrometer"
    tool_info.manufacturer = "Keysight Technologies"
    tool_info.model = "B2981A"
    
    return tool_info

@pytest.fixture
def info_keysight_b2893():
    tool_info = ToolInfo()

    tool_info.family = "electrometer"
    tool_info.manufacturer = "Keysight Technologies"
    tool_info.model = "B2983A"
    
    return tool_info

@pytest.fixture
def info_keysight_b2895():
    tool_info = ToolInfo()

    tool_info.family = "electrometer"
    tool_info.manufacturer = "Keysight Technologies"
    tool_info.model = "B2985A"
    
    return tool_info

@pytest.fixture
def info_keysight_b2897():
    tool_info = ToolInfo()

    tool_info.family = "electrometer"
    tool_info.manufacturer = "Keysight Technologies"
    tool_info.model = "B2987A"
    
    return tool_info


# Keysight factory
def test_get_keysight_tool(info_unknown, info_keysight_b2891):
    with pytest.raises(ValueError):
        keysight_factory.get_keysight_tool(info_unknown)
    
    test_electrometer = keysight_factory.get_keysight_tool(info_keysight_b2891)
    assert isinstance(test_electrometer, b298x.B2981)
    
def test_get_keysight_electrometer(info_unknown, info_keysight_b2891, info_keysight_b2893, info_keysight_b2895, info_keysight_b2897):
    with pytest.raises(ValueError):
        keysight_factory.get_keysight_electrometer(info_unknown)
    
    test_electrometer = keysight_factory.get_keysight_electrometer(info_keysight_b2891)
    assert isinstance(test_electrometer, b298x.B2981)

    test_electrometer = keysight_factory.get_keysight_electrometer(info_keysight_b2893)
    assert isinstance(test_electrometer, b298x.B2983)

    test_electrometer = keysight_factory.get_keysight_electrometer(info_keysight_b2895)
    assert isinstance(test_electrometer, b298x.B2985)

    test_electrometer = keysight_factory.get_keysight_electrometer(info_keysight_b2897)
    assert isinstance(test_electrometer, b298x.B2987)
