
R-testbench
===========



**R-testbench** is a toolkit written in Python that allows the user to 
create a software remote test bench to control an actual electronic test bench remotely.
It relies on the VISA protocol ([Virtual Instrument Software Architecture](http://www.ni.com/visa/)).
The implementation is built on top of [PyVISA](https://pyvisa.readthedocs.io/en/latest/).



Quick start
-----------


To use **R-testbench**, you simply need to import the *rtestbench* Python package.
```python
import rtestbench
```
Then you create an instance of `RTestBench`, that is basically the high-level interface/manager of the application.
```python
rtb = rtestbench.RTestBench()
```
Finally, you attach your instrument (resource) to `RTestBench` by passing the address of the instrument.
Connection between the computer and the instrument can be made by USB, LAN (Ethernet, WiFi), GPIB or RS232.
```python
instr = rtb.attach_resource(ADDR_INSTR)
```
**R-testbench** performs *automatic instrument recognition*.
You can check the current status of the project and an exhaustive list of supported instruments below.
If your instrument is not implemented in the toolkit, you can create a generic Tool and send raw commands.
In that case, please consider contributing by either writing the specific class or
sending me your script which contains the raw commands.

Tutorial scripts are available [here](./rtestbench/tutorials/).
This is a user-friendly way to start with the toolkit.



Current status
--------------


Until now, **R-testbench** has been developed to control the Keysight B2985A Electrometer.
However, I built the whole software architecture so that it can be extended to any instrument from any manufacturer.

If you would like to contribute to the project,
please read the [contribution guidelines](https://github.com/Arkh42/rtestbench/blob/master/CONTRIBUTING.md).
You can also contact me by [email](mailto:aquenon@hotmail.be).


### List of supported devices

List of devices currently supported in **R-testbench**, sorted by manufacturer:
- Agilent
- GW Instek
- Keysight:
	- B2981A (Electrometer)
	- B2983A (Electrometer)
	- B2985A (Electrometer)
	- B2987A (Electrometer)
- Rigol
- Rohde & Schwarz
- Siglent
- Tektronix
- Tenma
