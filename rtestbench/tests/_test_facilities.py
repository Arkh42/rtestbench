
# VISA library
import visa


def attach_simulated_device_to(tool):
    """Create a simulated VISA resource and attach it to a tool."""
    rm = visa.ResourceManager('@sim')
    sim_visa_resource = rm.open_resource('ASRL1::INSTR')
    tool.attach_visa_resource(sim_visa_resource)
