"""Test for the core module."""


import pytest

import visa
import numpy as np

import rtestbench


##########################
# Generic tool interface #
##########################

@pytest.fixture
def toolInfo_empty():
    """Returns an empty ToolInfo object, i.e., with all fields equal to None."""

    from rtestbench.core import ToolInfo
    return ToolInfo()

@pytest.fixture
def toolProperties_empty():
    """Returns an empty ToolProperties object, i.e., with default values."""

    from rtestbench.core import ToolProperties
    return ToolProperties()

@pytest.fixture
def toolFactory():
    """Returns a ToolFactory object with pyvisa-sim to enable a simulated resource."""

    from rtestbench.core import ToolFactory

    manager = visa.ResourceManager(visa_library='@sim')
    return ToolFactory(tool_manager=manager)

@pytest.fixture
def fakeToolWithoutInterface():

    from rtestbench.core import Tool
    from rtestbench.core import ToolInfo

    info = ToolInfo()
    info.manufacturer = "Toto Tester"
    info.model = "No interface"
    info.serial_number = "42"
    info.software_version = "3.x"

    return Tool(info)

@pytest.fixture
def fakeTool(toolFactory):
    from rtestbench.core import Tool
    from rtestbench.core import ToolInfo

    info = ToolInfo()
    info.manufacturer = "Toto Tester"
    info.model = "Simulated interface"
    info.serial_number = "42"
    info.software_version = "3.x"

    fake_tool = Tool(info)
    tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    fake_tool.connect_virtual_interface(tool_interface)

    return fake_tool

# --------

def test_toolInfo_attributes(toolInfo_empty):
    assert hasattr(toolInfo_empty, "family")
    assert hasattr(toolInfo_empty, "manufacturer")
    assert hasattr(toolInfo_empty, "model")
    assert hasattr(toolInfo_empty, "serial_number")
    assert hasattr(toolInfo_empty, "software_version")
    assert hasattr(toolInfo_empty, "interface")

def test_toolInfo_init(toolInfo_empty):
    assert toolInfo_empty.family is None
    assert toolInfo_empty.manufacturer is None
    assert toolInfo_empty.model is None
    assert toolInfo_empty.serial_number is None
    assert toolInfo_empty.software_version is None
    assert toolInfo_empty.interface is None

def test_toolInfo_interface(toolInfo_empty):
    toolInfo_empty.interface = visa.constants.InterfaceType.gpib
    assert toolInfo_empty.interface == "GPIB"
    toolInfo_empty.interface = visa.constants.InterfaceType.vxi
    assert toolInfo_empty.interface == "VXI, VME or MXI"
    toolInfo_empty.interface = visa.constants.InterfaceType.gpib_vxi
    assert toolInfo_empty.interface == "GPIB VXI"
    toolInfo_empty.interface = visa.constants.InterfaceType.asrl
    assert toolInfo_empty.interface == "Serial (RS-232 or RS-485)"
    toolInfo_empty.interface = visa.constants.InterfaceType.pxi
    assert toolInfo_empty.interface == "PXI"
    toolInfo_empty.interface = visa.constants.InterfaceType.tcpip
    assert toolInfo_empty.interface == "TCP/IP"
    toolInfo_empty.interface = visa.constants.InterfaceType.usb
    assert toolInfo_empty.interface == "USB"
    toolInfo_empty.interface = visa.constants.InterfaceType.rio
    assert toolInfo_empty.interface == "Rio"
    toolInfo_empty.interface = visa.constants.InterfaceType.firewire
    assert toolInfo_empty.interface == "Firewire"
    toolInfo_empty.interface = visa.constants.InterfaceType.rsnrp
    assert toolInfo_empty.interface == "Rohde & Schwarz Device via Passport"
    toolInfo_empty.interface = visa.constants.InterfaceType.unknown
    assert toolInfo_empty.interface == "Unknown"

    with pytest.raises(ResourceWarning):
        toolInfo_empty.interface = "toto"

# --------

def test_toolProperties_attributes(toolProperties_empty):
    assert hasattr(toolProperties_empty, "data_container")
    assert hasattr(toolProperties_empty, "transfer_formats")
    assert hasattr(toolProperties_empty, "bin_data_header")
    assert hasattr(toolProperties_empty, "endian")

def test_toolProperties_init(toolProperties_empty):
    assert toolProperties_empty.data_container is np.ndarray
    assert toolProperties_empty.transfer_formats == []
    assert toolProperties_empty.bin_data_header is None
    assert toolProperties_empty.endian is None

def test_toolProperties_datacontainer(toolProperties_empty):
    # Permitted values
    toolProperties_empty.data_container = list
    assert toolProperties_empty.data_container is list
    toolProperties_empty.data_container = tuple
    assert toolProperties_empty.data_container is tuple
    toolProperties_empty.data_container = np.ndarray
    assert toolProperties_empty.data_container is np.ndarray

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.data_container = float
        toolProperties_empty.data_container = str

def test_toolProperties_transferformats(toolProperties_empty):
    # Permitted values
    toolProperties_empty.transfer_formats = ['text']
    assert toolProperties_empty.transfer_formats == ['text']
    toolProperties_empty.transfer_formats = ['ascii']
    assert toolProperties_empty.transfer_formats == ['ascii']
    toolProperties_empty.transfer_formats = ['bin']
    assert toolProperties_empty.transfer_formats == ['bin']
    toolProperties_empty.transfer_formats = ['bin32']
    assert toolProperties_empty.transfer_formats == ['bin32']
    toolProperties_empty.transfer_formats = ['bin64']
    assert toolProperties_empty.transfer_formats == ['bin64']

    # Combination of permitted values
    toolProperties_empty.transfer_formats = ['text', 'bin']
    assert toolProperties_empty.transfer_formats == ['text', 'bin']
    toolProperties_empty.transfer_formats = ['ascii', 'bin32', 'bin64']
    assert toolProperties_empty.transfer_formats == ['ascii', 'bin32', 'bin64']

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.transfer_formats = ['toto']
        toolProperties_empty.transfer_formats = ['toto', 'text']
        toolProperties_empty.transfer_formats = ['text', 'toto']

def test_toolProperties_endian(toolProperties_empty):
    # Permitted values
    toolProperties_empty.endian = 'big'
    assert toolProperties_empty.endian == 'big'
    toolProperties_empty.endian = 'little'
    assert toolProperties_empty.endian == 'little'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.endian = 'toto'

# --------

def test_toolFactory_attributes(toolFactory):
    assert hasattr(toolFactory, "_tool_manager")

def test_toolFactory_findtool(toolFactory):
    # Correct address
    fake_tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    assert isinstance(fake_tool_interface, visa.Resource)

    # Incorrect interface
    with pytest.raises(AttributeError):
        fake_tool_interface = toolFactory._find_tool("toto::INSTR")
    
    # Error in address format
    with pytest.raises(ValueError):
        fake_tool_interface = toolFactory._find_tool("ASRL1:INSTR") 

def test_toolFactory_identifytool(toolFactory):
    # Tool device that can be reached
    fake_tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    tool_id = toolFactory._identify_tool(fake_tool_interface)
    assert isinstance(tool_id, str)

    # Tool device that cannot be reached
    fake_tool_interface = toolFactory._find_tool("TCPIP0::localhost::inst0::INSTR")
    with pytest.raises(IOError):
        tool_id = toolFactory._identify_tool(fake_tool_interface)

def test_toolFactory_parsetoolid(toolFactory):
    fake_tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    tool_id = toolFactory._identify_tool(fake_tool_interface)
    with pytest.raises(ValueError):
        tool_info = toolFactory._parse_tool_id(tool_id)

# --------

def test_tool_connectVirtualInterface(toolFactory, fakeToolWithoutInterface):
    # Wrong tool interface
    with pytest.raises(AttributeError):
        fakeToolWithoutInterface.connect_virtual_interface(42)

    # Interface without valid session
    tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    tool_interface.close()
    with pytest.raises(IOError):
        fakeToolWithoutInterface.connect_virtual_interface(tool_interface)
    
    # Correct interface
    tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    fakeToolWithoutInterface.connect_virtual_interface(tool_interface)
    assert fakeToolWithoutInterface._info.interface == "Serial (RS-232 or RS-485)"

    # Connection while there is already an interface
    with pytest.raises(RuntimeError):
        fakeToolWithoutInterface.connect_virtual_interface(tool_interface)

def test_tool_disconnectVirtualInterface(toolFactory, fakeTool):
    assert fakeTool._virtual_interface is not None
    fakeTool.disconnect_virtual_interface()
    assert fakeTool._virtual_interface is None

def test_tool_send(toolFactory, fakeToolWithoutInterface, fakeTool):
    # No virtual interface
    with pytest.raises(UnboundLocalError):
        fakeToolWithoutInterface.send('command')
    
    # Send command (no exception raised by simulated device)
    fakeTool.send('command')
    

def test_tool_query(toolFactory, fakeToolWithoutInterface, fakeTool):
    # No virtual interface
    with pytest.raises(UnboundLocalError):
        fakeToolWithoutInterface.query('request')
    
    # Send request (no exception raised by simulated device)
    answer = fakeTool.query("*IDN?")
    assert isinstance(answer, str)




#######################
# R-testbench manager #
#######################

@pytest.fixture
def rtb_quiet():
    """Returns a non-verbose RTestBench."""

    import logging
    from rtestbench.core import RTestBenchManager

    rtb = RTestBenchManager(verbose=False, visa_library='')
    logging.disable(logging.CRITICAL)

    return rtb

@pytest.fixture
def rtb_simulated_visaRM():
    """Returns a non-verbose RTestBench with a simulated VISA resource manager."""

    from rtestbench.core import RTestBenchManager

    rtb = RTestBenchManager(verbose=False, visa_library='@sim')

    return rtb


# Constructor
def test_initialize(rtb_simulated_visaRM):
    assert hasattr(rtb_simulated_visaRM, "_VERBOSE")
    assert hasattr(rtb_simulated_visaRM, "_attached_tools")
    assert hasattr(rtb_simulated_visaRM, "chat")
    assert hasattr(rtb_simulated_visaRM, "logger")


# Destructor and related close functions
def test_close_visa_rm(rtb_simulated_visaRM):
    assert rtb_simulated_visaRM._visa_rm is not None
    rtb_simulated_visaRM._close_visa_rm()
    assert rtb_simulated_visaRM._visa_rm is None


# Information about tools
def test_detect_tools(rtb_simulated_visaRM):
    detected_tools = rtb_simulated_visaRM.detect_tools()
    assert detected_tools
    assert isinstance(detected_tools, tuple)


# Tools management
# def test_attach_tool(sim_visa_rm, rtb_quiet):
#     with pytest.raises(ValueError):
#         rtb_quiet.attach_tool('ASRL1::INSTR')
