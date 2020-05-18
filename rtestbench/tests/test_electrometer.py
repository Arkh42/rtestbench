"""Test for the electrometer module."""


import pytest


@pytest.fixture
def fakeElectrometerWithoutInterface():

    from rtestbench.tools.electrometer import Electrometer
    from rtestbench.core import ToolInfo

    info = ToolInfo()
    info.manufacturer = "Toto Tester"
    info.model = "No interface"
    info.serial_number = "42"
    info.software_version = "3.x"

    return Electrometer(info)


def test_electrometer_init(fakeElectrometerWithoutInterface):
    assert hasattr(fakeElectrometerWithoutInterface, "_info")
    assert hasattr(fakeElectrometerWithoutInterface, "_properties")
    assert hasattr(fakeElectrometerWithoutInterface, "_virtual_interface")

    assert fakeElectrometerWithoutInterface._info.family == "electrometer"

def test_electrometer_interface(fakeElectrometerWithoutInterface):
    # Scale and offset interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_scale(axis=1, scale=10)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_offset(axis=1, offset=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_xscale(scale=10)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_yscale(scale=10)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_xoffset(offset=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_yoffset(offset=42)
    # Range interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_range(value=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_autorange(switch=True)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_range_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_range_max()
    # Aperture (integration) time interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_aperture_time(value=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_integration_time(value=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_aperture_time_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_aperture_time_max()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_integration_time_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_integration_time_max()
