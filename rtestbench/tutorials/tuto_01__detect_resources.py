
# R-testbench toolkit
import rtestbench



# Step 1 - create the software remote test bench
rtb = rtestbench.RTestBenchManager()


# Step 2 - detect available resources
available_resources = rtb.detect_resources()

# Step 3 - print the results
if available_resources:
    print('Available resources:', available_resources)
else:
    print('No available resources')

print('Variable type:', type(available_resources), '\n')


# Alternative to steps 2 and 3
rtb.print_available_resources()


# Step 4 - close everything properly
rtb.close()
