
import sys

import rtestbench


# Step 1 - create the software remote test bench
testbench = rtestbench.Manager()

# Step 2 - attach your tool (instrument) to the test bench
instr_1 = None
instr_2 = None

ADDR_INSTR_1 = "no::instrument" # uncomment to go inside the else/except
ADDR_INSTR_2 = "USB0::0x0957::0x9318::MY54321248::0::INSTR" # example of tool address


# 1st method: if/else
if ADDR_INSTR_1 in testbench.detect_tools():
    instr_1 = testbench.attach_tool(ADDR_INSTR_1)
else:
    testbench.log_warning("It seems that there is no instrument @ {}.".format(ADDR_INSTR_1))

# 2nd method: try/except
try:
    instr_2 = testbench.attach_tool(ADDR_INSTR_2)
except ValueError as err:
    testbench.log_warning(err)

if instr_2 is None:
    testbench.log_critical("Cannot continue without an instrument... Abort!")
    sys.exit()

# Step 3 - set the format of data transfer
try:
    instr_2.set_data_transfer_format(tsf_format="text", data_type="float")
except (NotImplementedError, ValueError, RuntimeError) as err:
    testbench.log_error(err)

# Step 4 - send raw commands to your resource
try:
    id_instr = instr_2.query("*IDN?") # generic command available for all instruments
    temperature = instr_2.query_data(":SYSTem:TEMPerature?") # command specific to Keysight B2895A/B2987A electrometers
except (UnboundLocalError, IOError, RuntimeError) as err:
    testbench.log_error(err)
else:
    testbench.log_info("Instrument ID = {}.".format(id_instr))
    testbench.log_info("Variable type of Instrument ID is {} because of query().".format(type(id_instr)))
    testbench.log_info("Temperature = {}.".format(temperature))
    testbench.log_info("Variable type of Temperature is {} because of query_data().".format(type(temperature)))

# Step 4 - close everything properly
testbench.close()
