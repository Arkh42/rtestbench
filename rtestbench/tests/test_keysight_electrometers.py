"""Test for the Keysight electrometer modules."""


import pytest
import visa

from rtestbench import constants
from rtestbench.core import ToolInfo
from rtestbench.core import ToolFactory
from rtestbench.tools.keysight.electrometer import b298x


@pytest.fixture
def fakeB298xWithoutInterface():
    info = ToolInfo()
    info.serial_number = "42"
    info.software_version = "3.x"

    return b298x.B298X(info)

@pytest.fixture
def realB2985(address):
    tool_factory = ToolFactory(visa.ResourceManager())
    electrometer = tool_factory.get_tool(address)
    return electrometer


def test_B298X_init_info(fakeB298xWithoutInterface):
    assert fakeB298xWithoutInterface._info.family == "electrometer"

def test_B298X_init_properties(fakeB298xWithoutInterface):
    assert fakeB298xWithoutInterface._properties.transfer_formats == constants.RTB_TRANSFERT_FORMATS

    assert fakeB298xWithoutInterface._properties.bin_data_endianness == "big"
    assert fakeB298xWithoutInterface._properties.bin_data_header == "ieee"
    assert fakeB298xWithoutInterface._properties.bin_data_type == 'f'

    assert fakeB298xWithoutInterface._properties.read_msg_terminator == '\n'
    assert fakeB298xWithoutInterface._properties.write_msg_terminator == '\n'

    assert fakeB298xWithoutInterface._properties.text_data_converter == 'e'
    assert fakeB298xWithoutInterface._properties.text_data_separator == ','


    assert fakeB298xWithoutInterface._properties.activated_view_mode == None
    assert fakeB298xWithoutInterface._properties.activated_subview_mode == None


@pytest.mark.keysight_b2985
def test_B2985_init(realB2985):
    assert realB2985._info.family == "electrometer"
    assert realB2985._info.manufacturer == "Keysight Technologies"
    assert realB2985._info.model == "B2985"
