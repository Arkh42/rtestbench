
R-testbench
===========



**R-testbench** is a toolkit written in Python that allows the user to 
create a software remote test bench to control an actual electronic test bench remotely.
It relies on the VISA protocol ([Virtual Instrument Software Architecture](http://www.ni.com/visa/)).
The implementation is built on top of [PyVISA](https://pyvisa.readthedocs.io/en/latest/).



Installation
------------

The installation is a 2-step process:
1. clone the git repository
2. install the dependencies

```
git clone https://github.com/Arkh42/rtestbench
pip install -r rtestbench/requirements.txt
```

You are ready to start!



Quick start
-----------


To use **R-testbench**, you simply need to import the *rtestbench* Python package.
```python
import rtestbench
```

Then you create an instance of `RTestBenchManager`, that is basically the high-level interface/manager of the application.
```python
testbench = rtestbench.RTestBenchManager()
```
For easier use, the `RTestBenchManager` is also available as `Manager`, hence:
```python
testbench = rtestbench.Manager()
```

Finally, you attach your instrument (tool) to `RTestBenchManager` by passing the address of the instrument.
Connection between the computer and the instrument can be made by USB, LAN (Ethernet, WiFi), GPIB or serial.
```python
instr = testbench.attach_tool(ADDR_INSTR)
```

**R-testbench** performs *automatic instrument recognition*.
You can check the current status of the project and an exhaustive list of supported instruments below.
If your instrument is not implemented in the toolkit, a generic Tool is created so that you send raw SCPI commands.
In that case, please consider contributing by either writing the specific class or
sending me your script which contains the SCPI commands.

Tutorial scripts are available [here](./rtestbench/tutorials/).
This is a user-friendly way to start with the toolkit.



Current status
--------------


Until now, **R-testbench** has been developed to control the Keysight B2985A Electrometer.
However, I built the whole software architecture so that it can be extended to any instrument from any manufacturer.

If you would like to contribute to the project,
please read the [contribution guidelines](https://github.com/Arkh42/rtestbench/blob/master/CONTRIBUTING.md).
You can also contact me by [email](mailto:aquenon@hotmail.be).


### Code quality

![Continuous Integration (pip)](https://github.com/Arkh42/rtestbench/workflows/Continuous%20Integration%20(pip)/badge.svg?branch=master)
![Coverage](https://img.shields.io/coveralls/github/Arkh42/rtestbench/master)


### Statistics

![Language counts](https://img.shields.io/github/languages/count/Arkh42/rtestbench)
&bull;
![Top language](https://img.shields.io/github/languages/top/Arkh42/rtestbench)

[![Issues](https://img.shields.io/github/issues-raw/Arkh42/rtestbench)](https://github.com/Arkh42/rtestbench/issues?q=is%3Aopen+is%3Aissue)
&bull;
[![Issues closed](https://img.shields.io/github/issues-closed-raw/Arkh42/rtestbench)](https://github.com/Arkh42/rtestbench/issues?q=is%3Aissue+is%3Aclosed)



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



Organization of the package
---------------------------


The `rtestbench` package is organized with:
- features, which are 'public' modules that provide the main functionalities;
- utilities, which are 'private' modules that extend the capabilities of the package.

Current features are:
- `core`, the main module of R-testbench that regroups all functionalities.

Current utilities are:
- `_chat`, a message shaper for communication between app and user;
- `_logger`, a logger configurator for the application;
- `_meta`, a meta-data interface.
