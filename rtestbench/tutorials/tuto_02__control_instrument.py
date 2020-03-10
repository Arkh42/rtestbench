
# R-testbench toolkit
import rtestbench

import sys



# Step 1 - create the software remote test bench
rtb = rtestbench.RTestBenchManager()


# Step 2 - attach your resource (instrument) to the test bench
instr_1 = None
instr_2 = None

ADDR_INSTR = 'USB0::0x0957::0x9318::MY54321248::0::INSTR' # write the address of your instrument here
ADDR_INSTR = 'no::instrument' # uncomment to go inside the else/except


    # 1st solution
if ADDR_INSTR in rtb.detect_resources():
    instr_1 = rtb.attach_resource(ADDR_INSTR)
else:
    rtb.log_warning('It seems that there is no instrument @ {}.'.format(ADDR_INSTR))

    # 2nd solution
try:
    instr_2 = rtb.attach_resource(ADDR_INSTR)
except ValueError as error_msg:
    rtb.log_warning(error_msg)

if instr_1 is None and instr_2 is None:
    sys.exit('Cannot continue without an instrument... Abort!')

instr = None
if instr_2 is not None:
    instr = instr_2
else:
    instr = instr_1
    

# Step 3 - set the format of data transfer
try:
    if instr.transfer_format is None:
        instr.transfer_format = 'text'
    else:
        rtb.log_info('Default transfer format is text.\n\n')
except (NotImplementedError, ValueError) as error_msg:
    rtb.log_error(error_msg)


# Step 4 - send raw commands to your resource
translation_table = dict.fromkeys(map(ord, '\n'), None) # tip to remove newline termination character

try:
    id_instr = instr.query('*IDN?') # generic command available for all instruments
    temperature = instr.query_data(':SYSTem:TEMPerature?') # command specific to Keysight B2895A/B2987A electrometers
except (UnboundLocalError, RuntimeError) as error_msg:
    rtb.log_error(error_msg)
else:
    rtb.log_info('Instrument ID = {}'.format(id_instr.translate(translation_table)))
    rtb.log_info('Variable type of Instrument ID is {} because of query()\n'.format(type(id_instr)))
    rtb.log_info('Temperature = {}'.format(temperature))
    rtb.log_info('Variable type of Temperature is {} because of query_data()\n'.format(type(temperature)))


# Step 4 - close everything properly
rtb.close()
