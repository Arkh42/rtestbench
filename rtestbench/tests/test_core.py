"""Test for the core module."""


import logging
import pytest

import visa
import numpy as np

import rtestbench
from rtestbench import constants
from rtestbench.core import RTestBenchManager
from rtestbench.core import Tool
from rtestbench.core import ToolFactory
from rtestbench.core import ToolInfo
from rtestbench.core import ToolProperties


##########################
# Generic tool interface #
##########################

@pytest.fixture
def toolInfo_empty():
    """Returns an empty ToolInfo object, i.e., with all fields equal to None."""

    return ToolInfo()

@pytest.fixture
def toolProperties_empty():
    """Returns an empty ToolProperties object, i.e., with default values."""

    return ToolProperties()

@pytest.fixture
def toolFactory():
    """Returns a ToolFactory object with pyvisa-sim to enable a simulated resource."""

    manager = visa.ResourceManager(visa_library='@sim')
    return ToolFactory(tool_manager=manager)

@pytest.fixture
def tool_empty(toolInfo_empty):
    """Returns an empty Tool, i.e., with default values."""

    return Tool(toolInfo_empty)

@pytest.fixture
def fakeToolWithoutInterface():
    info = ToolInfo()
    info.manufacturer = "Toto Tester"
    info.model = "No interface"
    info.serial_number = "42"
    info.software_version = "3.x"

    return Tool(info)

@pytest.fixture
def fakeTool(toolFactory):
    info = ToolInfo()
    info.manufacturer = "Toto Tester"
    info.model = "Simulated interface"
    info.serial_number = "42"
    info.software_version = "3.x"

    fake_tool = Tool(info)
    fake_tool._properties.bin_data_header = "empty" # Necessary for the simulated device
    fake_tool._properties.write_msg_terminator = '\r\n' # Necessary for the simulated device
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

    toolInfo_empty.interface = None
    assert toolInfo_empty.interface is None

    with pytest.raises(ResourceWarning):
        toolInfo_empty.interface = "toto"

# --------

def test_toolProperties_attributes(toolProperties_empty):
    assert hasattr(toolProperties_empty, "data_container")
    assert hasattr(toolProperties_empty, "transfer_formats")
    assert hasattr(toolProperties_empty, "bin_data_header")
    assert hasattr(toolProperties_empty, "bin_data_endianness")
    assert hasattr(toolProperties_empty, "read_msg_terminator")
    assert hasattr(toolProperties_empty, "write_msg_terminator")
    assert hasattr(toolProperties_empty, "text_data_converter")
    assert hasattr(toolProperties_empty, "text_data_separator")
    assert hasattr(toolProperties_empty, "timeout")
    assert hasattr(toolProperties_empty, "activated_transfer_format")

def test_toolProperties_init(toolProperties_empty):
    assert toolProperties_empty.data_container is np.ndarray
    assert toolProperties_empty.transfer_formats == []
    assert toolProperties_empty.bin_data_header == "ieee"
    assert toolProperties_empty.bin_data_endianness == "little"
    assert toolProperties_empty.read_msg_terminator == '\n'
    assert toolProperties_empty.write_msg_terminator == '\n'
    assert toolProperties_empty.text_data_converter == 'f'
    assert toolProperties_empty.text_data_separator == ','
    assert toolProperties_empty.timeout == 0
    assert toolProperties_empty.activated_transfer_format is None

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
    with pytest.raises(ValueError):
        toolProperties_empty.data_container = str

def test_toolProperties_transferformats(toolProperties_empty):
    # Permitted values
    toolProperties_empty.transfer_formats = ['text']
    assert toolProperties_empty.transfer_formats == ['text']
    toolProperties_empty.transfer_formats = ['ascii']
    assert toolProperties_empty.transfer_formats == ['ascii']
    toolProperties_empty.transfer_formats = ['bin']
    assert toolProperties_empty.transfer_formats == ['bin']
    toolProperties_empty.transfer_formats = ['binary']
    assert toolProperties_empty.transfer_formats == ['binary']

    # Combination of permitted values
    toolProperties_empty.transfer_formats = ['text', 'bin']
    assert toolProperties_empty.transfer_formats == ['text', 'bin']
    toolProperties_empty.transfer_formats = ['ascii', 'bin', 'binary']
    assert toolProperties_empty.transfer_formats == ['ascii', 'bin', 'binary']

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.transfer_formats = ['toto']
    with pytest.raises(ValueError):
        toolProperties_empty.transfer_formats = ['toto', 'text']
    with pytest.raises(ValueError):
        toolProperties_empty.transfer_formats = ['text', 'toto']

def test_toolProperties_bindataendianess(toolProperties_empty):
    # Permitted values
    toolProperties_empty.bin_data_endianness = 'big'
    assert toolProperties_empty.bin_data_endianness == 'big'
    toolProperties_empty.bin_data_endianness = 'little'
    assert toolProperties_empty.bin_data_endianness == 'little'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.bin_data_endianness = 'toto'

def test_toolProperties_bindataheader(toolProperties_empty):
    # Permitted values
    toolProperties_empty.bin_data_header = 'ieee'
    assert toolProperties_empty.bin_data_header == 'ieee'
    toolProperties_empty.bin_data_header = 'empty'
    assert toolProperties_empty.bin_data_header == 'empty'
    toolProperties_empty.bin_data_header = 'hp'
    assert toolProperties_empty.bin_data_header == 'hp'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.bin_data_header = 'toto'

def test_toolProperties_bindatatype(toolProperties_empty):
    # Permitted values
    toolProperties_empty.bin_data_type = 'f'
    assert toolProperties_empty.bin_data_type == 'f'
    toolProperties_empty.bin_data_type = "bin64"
    assert toolProperties_empty.bin_data_type == 'd'
    toolProperties_empty.bin_data_type = "short"
    assert toolProperties_empty.bin_data_type == 'h'
    toolProperties_empty.bin_data_type = "int"
    assert toolProperties_empty.bin_data_type == 'i'
    toolProperties_empty.bin_data_type = "long long"
    assert toolProperties_empty.bin_data_type == 'q'
    toolProperties_empty.bin_data_type = 'H'
    assert toolProperties_empty.bin_data_type == 'H'
    toolProperties_empty.bin_data_type = "unsigned int"
    assert toolProperties_empty.bin_data_type == 'I'
    toolProperties_empty.bin_data_type = "uint64"
    assert toolProperties_empty.bin_data_type == 'Q'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.bin_data_type = "toto"

def test_toolProperties_parsemsgterminator(toolProperties_empty):
    # Permitted values
    assert toolProperties_empty.parse_msg_terminator('\n') == '\n'
    assert toolProperties_empty.parse_msg_terminator('LF') == '\n'
    assert toolProperties_empty.parse_msg_terminator('NL') == '\n'
    assert toolProperties_empty.parse_msg_terminator("CRLF") == '\r\n'
    assert toolProperties_empty.parse_msg_terminator("carriage return") == '\r'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.parse_msg_terminator("toto")

def test_toolProperties_readmsgterminator(toolProperties_empty):
    # Permitted values
    toolProperties_empty.read_msg_terminator = "line feed"
    assert toolProperties_empty.read_msg_terminator == '\n'
    toolProperties_empty.read_msg_terminator = "CR"
    assert toolProperties_empty.read_msg_terminator == '\r'
    toolProperties_empty.read_msg_terminator = "CRLF"
    assert toolProperties_empty.read_msg_terminator == '\r\n'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.read_msg_terminator = "toto"

def test_toolProperties_writemsgterminator(toolProperties_empty):
    # Permitted values
    toolProperties_empty.write_msg_terminator = "newline"
    assert toolProperties_empty.write_msg_terminator == '\n'
    toolProperties_empty.write_msg_terminator = '\r'
    assert toolProperties_empty.write_msg_terminator == '\r'
    toolProperties_empty.write_msg_terminator = '\r\n'
    assert toolProperties_empty.write_msg_terminator == '\r\n'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.write_msg_terminator = "toto"

def test_toolProperties_textdataconverter(toolProperties_empty):
    # Permitted values
    toolProperties_empty.text_data_converter = 'b' 
    assert toolProperties_empty.text_data_converter == 'b'
    toolProperties_empty.text_data_converter = "oct"
    assert toolProperties_empty.text_data_converter == 'o'
    toolProperties_empty.text_data_converter = "hexadecimal"
    assert toolProperties_empty.text_data_converter == 'x'
    toolProperties_empty.text_data_converter = 'd'
    assert toolProperties_empty.text_data_converter == 'd'
    toolProperties_empty.text_data_converter = "fix"
    assert toolProperties_empty.text_data_converter == 'f'
    toolProperties_empty.text_data_converter = "exponent"
    assert toolProperties_empty.text_data_converter == 'e'
    toolProperties_empty.text_data_converter = 's'
    assert toolProperties_empty.text_data_converter == 's'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.text_data_converter = "toto"  

def test_toolProperties_textdataseparator(toolProperties_empty):
    # Permitted values
    toolProperties_empty.text_data_separator = ',' 
    assert toolProperties_empty.text_data_separator == ','
    toolProperties_empty.text_data_separator = ';'
    assert toolProperties_empty.text_data_separator == ';'
    toolProperties_empty.text_data_separator = ' '
    assert toolProperties_empty.text_data_separator == ' '

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.text_data_separator = "."    

def test_toolProperties_timeout(toolProperties_empty):
    # Special values
    toolProperties_empty.timeout = "infinite"
    assert toolProperties_empty.timeout == float('+inf')
    toolProperties_empty.timeout = "immediate"
    assert toolProperties_empty.timeout == 0

    # Float
    toolProperties_empty.timeout = 42
    assert toolProperties_empty.timeout == 42

def test_toolProperties_activatedtransferformat(toolProperties_empty):
    # No available formats
    with pytest.raises(ValueError):
        toolProperties_empty.activated_transfer_format = "bin"
    
    # One available format
    toolProperties_empty.transfer_formats = ["bin"]
    toolProperties_empty.activated_transfer_format = "bin"
    assert toolProperties_empty.activated_transfer_format == "bin"
    with pytest.raises(ValueError):
        toolProperties_empty.activated_transfer_format = "toto"
    
    # All available formats
    toolProperties_empty.transfer_formats = constants.RTB_TRANSFERT_FORMATS
    toolProperties_empty.activated_transfer_format = "bin"
    assert toolProperties_empty.activated_transfer_format == "bin"
    toolProperties_empty.activated_transfer_format = "text"
    assert toolProperties_empty.activated_transfer_format == "text"
    with pytest.raises(ValueError):
        toolProperties_empty.activated_transfer_format = "toto"


def test_toolProperties_getproperties(toolProperties_empty):
    assert toolProperties_empty.get_properties() == toolProperties_empty.__dict__

def test_toolProperties_updateproperties(toolProperties_empty):
    toolProperties_empty.update_properties(tester="toto")
    assert hasattr(toolProperties_empty, "tester")
    assert toolProperties_empty.tester == "toto"

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
    # Failing parsing
    fake_tool_interface = toolFactory._find_tool("ASRL1::INSTR")
    tool_id = toolFactory._identify_tool(fake_tool_interface)
    with pytest.raises(ValueError):
        tool_info = toolFactory._parse_tool_id(tool_id)
    
    # Correct parsing
    tool_id = "Manufacturer,model,serial,revision"
    tool_info = toolFactory._parse_tool_id(tool_id)
    assert isinstance(tool_info, ToolInfo)
    assert tool_info.manufacturer == "Manufacturer"
    assert tool_info.model == "model"
    assert tool_info.serial_number == "serial"
    assert tool_info.software_version == "revision"

def test_toolFactory_buildspecifictool(toolFactory, fakeTool):
    # Unknown manufacturer
    with pytest.raises(NotImplementedError):
        toolFactory._build_specific_tool(fakeTool._info)
    
    # Known manufacturer but unknown model
    fakeTool._info.manufacturer = "Keysight Technologies"
    with pytest.raises(ValueError):
        toolFactory._build_specific_tool(fakeTool._info)

def test_toolFactory_buildgenerictool(toolFactory, fakeTool):
    new_tool = toolFactory._build_generic_tool(fakeTool._info)
    assert isinstance(new_tool, Tool)
    assert new_tool._info == fakeTool._info

def test_toolFactory_get_tool(toolFactory):
    # Incorrect interface
    with pytest.raises(AttributeError):
        test_tool = toolFactory.get_tool("toto::INSTR")
    
    # Error in address format
    with pytest.raises(ValueError):
        test_tool = toolFactory.get_tool("ASRL1:INSTR")
    
    # Tool device that cannot be reached
    with pytest.raises(IOError):
        test_tool = toolFactory.get_tool("TCPIP0::localhost::inst0::INSTR")

    # Tool that answers but cannot be parsed
    with pytest.raises(ValueError):
        test_tool = toolFactory.get_tool("ASRL1::INSTR")


# --------

def test_tool_init(tool_empty):
    assert hasattr(tool_empty, "_info")
    assert hasattr(tool_empty, "_properties")
    assert hasattr(tool_empty, "_virtual_interface")

def test_tool_properties(tool_empty, toolProperties_empty):
    assert tool_empty._properties.data_container == toolProperties_empty.data_container
    assert tool_empty._properties.transfer_formats == toolProperties_empty.transfer_formats
    assert tool_empty._properties.bin_data_header == toolProperties_empty.bin_data_header
    assert tool_empty._properties.bin_data_endianness == toolProperties_empty.bin_data_endianness
    assert tool_empty._properties.text_data_converter == toolProperties_empty.text_data_converter
    assert tool_empty._properties.text_data_separator == toolProperties_empty.text_data_separator
    assert tool_empty._properties.timeout == toolProperties_empty.timeout
    assert tool_empty._properties.activated_transfer_format == toolProperties_empty.activated_transfer_format


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
    assert fakeToolWithoutInterface._virtual_interface.read_termination == fakeToolWithoutInterface._properties.read_msg_terminator
    assert fakeToolWithoutInterface._virtual_interface.write_termination == fakeToolWithoutInterface._properties.write_msg_terminator

    # Connection while there is already an interface
    with pytest.raises(RuntimeError):
        fakeToolWithoutInterface.connect_virtual_interface(tool_interface)

def test_tool_disconnectVirtualInterface(fakeTool):
    assert fakeTool._virtual_interface is not None
    fakeTool.disconnect_virtual_interface()
    assert fakeTool._virtual_interface is None

def test_tool_send(fakeToolWithoutInterface, fakeTool):
    # No virtual interface
    with pytest.raises(UnboundLocalError):
        fakeToolWithoutInterface.send('command')
    
    # Send command (no exception raised by simulated device)
    fakeTool.send('command')

    # DOES NOT WORK - Change write termination character to generate visa.VisaIOError
    # fakeTool._virtual_interface.write_termination = '\r'
    # with pytest.raises(IOError):
    #     answer = fakeTool.send("command")

    # Close virtual interface to generate visa.InvalidSession
    fakeTool._virtual_interface.close()
    with pytest.raises(RuntimeError):
        fakeTool.send('command')
    
def test_tool_query(fakeToolWithoutInterface, fakeTool):
    # No virtual interface
    with pytest.raises(UnboundLocalError):
        fakeToolWithoutInterface.query('request')
    
    # Send request (no exception raised by simulated device)
    answer = fakeTool.query("*IDN?")
    assert isinstance(answer, str)

    # Change read termination character to generate visa.VisaIOError
    fakeTool._virtual_interface.read_termination = '\r'
    with pytest.raises(IOError):
        answer = fakeTool.query("*IDN?")

    # Close virtual interface to generate visa.InvalidSession
    fakeTool._virtual_interface.close()
    with pytest.raises(RuntimeError):
        fakeTool.query("*IDN?")

def test_tool_querydata(fakeToolWithoutInterface, fakeTool):
    # No virtual interface
    with pytest.raises(UnboundLocalError):
        fakeToolWithoutInterface.query_data('request')

    # No transfer format
    with pytest.raises(UnboundLocalError):
        fakeTool.query_data('request')

    # Activated transfer format
    fakeTool._properties.transfer_formats = constants.RTB_TRANSFERT_FORMATS

    fakeTool._properties.activated_transfer_format = "text"
    data = fakeTool.query_data('request')

    fakeTool._properties.activated_transfer_format = "ascii"
    data = fakeTool.query_data('request')

    fakeTool._properties.activated_transfer_format = "bin"
    data = fakeTool.query_data('request')

    fakeTool._properties.activated_transfer_format = "binary"
    data = fakeTool.query_data('request')

    # Change read termination character to generate visa.VisaIOError
    fakeTool._virtual_interface.read_termination = '\r'
    with pytest.raises(IOError):
        answer = fakeTool.query_data('request')

    # Unsupported transfer formats
    fakeTool._properties._transfer_formats = "toto" # for test purpose only
    fakeTool._properties.activated_transfer_format = "toto"
    with pytest.raises(NotImplementedError):
        data = fakeTool.query_data('request')

    # Close virtual interface to generate visa.InvalidSession
    fakeTool._virtual_interface.close()
    with pytest.raises(RuntimeError):
        fakeTool.query_data('request')


def test_tool_set_timeout(fakeTool):
    fakeTool.set_timeout(42)
    assert fakeTool._properties.timeout == 42
    assert fakeTool._virtual_interface.timeout == 42

def test_tool_set_data_transfer_format(fakeTool):
    with pytest.raises(NotImplementedError):
        fakeTool.set_data_transfer_format("bin", "bin32")

def test_tool_clear_status(fakeTool):
    fakeTool.clear_status()

def test_tool_reset(fakeTool):
    fakeTool.reset()

def test_tool_lock(fakeTool):
    with pytest.raises(NotImplementedError):
        fakeTool.lock()

def test_tool_unlock(fakeTool):
    with pytest.raises(NotImplementedError):
        fakeTool.unlock()



#######################
# R-testbench manager #
#######################

@pytest.fixture
def rtb_quiet():
    """Returns a non-verbose RTestBench."""

    rtb = RTestBenchManager(verbose=False, visa_library='')
    logging.disable(logging.CRITICAL)

    return rtb

@pytest.fixture
def rtb_simulated_visaRM():
    """Returns a non-verbose RTestBench with a simulated VISA resource manager."""

    rtb = RTestBenchManager(verbose=False, visa_library='@sim')
    logging.disable(logging.CRITICAL)

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

def test_print_available_tools(capsys, rtb_simulated_visaRM):
    rtb_simulated_visaRM.print_available_tools()
    assert "ASRL1::INSTR" in capsys.readouterr().out


# Tools management
def test_attach_tool(rtb_simulated_visaRM):
    # Incorrect interface
    with pytest.raises(ValueError):
        test_tool = rtb_simulated_visaRM.attach_tool("toto::INSTR")
    
    # Error in address format
    with pytest.raises(ValueError):
        test_tool = rtb_simulated_visaRM.attach_tool("ASRL1:INSTR")
    
    # Tool device that cannot be reached
    with pytest.raises(ValueError):
        test_tool = rtb_simulated_visaRM.attach_tool("TCPIP0::localhost::inst0::INSTR")

    # Tool that answers but cannot be parsed
    with pytest.raises(ValueError):
        test_tool = rtb_simulated_visaRM.attach_tool("ASRL1::INSTR")
