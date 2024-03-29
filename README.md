
R-testbench
===========


<p align="center">
	<a href="https://travis-ci.org/github/Arkh42/rtestbench">
		<img alt="Build Status" src="https://travis-ci.org/Arkh42/rtestbench.svg?branch=master">
	</a>
	<a href='https://rtestbench.readthedocs.io/en/latest/?badge=latest'>
		<img src='https://readthedocs.org/projects/rtestbench/badge/?version=latest' alt='Documentation Status' />
	</a>
	<a href="https://github.com/Arkh42/rtestbench/actions">
		<img alt="Actions Status" src="https://github.com/Arkh42/rtestbench/workflows/Continuous%20Integration%20(pip)/badge.svg?branch=master">
	</a>
	<a href="https://codecov.io/gh/Arkh42/rtestbench">
		<img alt="Coverage Status" src="https://codecov.io/gh/Arkh42/rtestbench/branch/master/graph/badge.svg">
	</a>
	<a href="https://github.com/Arkh42/rtestbench/blob/master/LICENSE.md">
		<img alt="License: OSL" src="https://img.shields.io/github/license/Arkh42/rtestbench">
	</a>
</p>

---


**R-testbench** is a toolkit written in Python that allows the user to 
create a software remote test bench to control an actual electronic test bench remotely.
It relies on the VISA protocol ([Virtual Instrument Software Architecture](http://www.ni.com/visa/)).
The implementation is built on top of [PyVISA](https://pyvisa.readthedocs.io/en/latest/).

---

_Contents:_ 
**[Installation](#installation)** |
**[Quick start](#quick-start)** |
**[Current status](#current-status)** |
**[Organization of the package](#organization-of-the-package)** |
**[Citation](#citation)**

---


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



### Statistics

![Language counts](https://img.shields.io/github/languages/count/Arkh42/rtestbench)
![Top language](https://img.shields.io/github/languages/top/Arkh42/rtestbench)

[![Issues](https://img.shields.io/github/issues-raw/Arkh42/rtestbench)](https://github.com/Arkh42/rtestbench/issues?q=is%3Aopen+is%3Aissue)
[![Issues closed](https://img.shields.io/github/issues-closed-raw/Arkh42/rtestbench)](https://github.com/Arkh42/rtestbench/issues?q=is%3Aissue+is%3Aclosed)


### Supported OS

The following operating systems have been tested.

| Distributions		| Versions 	| Tests					|
| :------------		| :------: 	| :----					|
| Windows 10   		|			| User (alpha test) 	|
| Windows Server	| 2019		| CI (GitHub)			|
| Linux Ubuntu		| 18.04  	| CI (GitHub)			|
|					| 16.04		| CI (GitHub, Travis)	|
| macOS   			| 10.15		| CI (GitHub)			|


### Supported Python versions

Currently, R-testbench supports Python 3.6, 3.7 and 3.8.


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
- `constants`, the module that defines all constants required in R-testbench;
- `core`, the main module of R-testbench that regroups all functionalities.

Current utilities are:
- `_chat`, a message shaper for communication between app and user;
- `_logger`, a logger configurator for the application;
- `_meta`, a meta-data interface.



Citation
--------


If you use this work in the frame of scientific publication, please cite the following article:

> A. Quenon, E. Daubie, V. Moeyaert, and F. Dualibe, “R-testbench: a Journey in Open Source Programming for Remote Instrumentation with Python,” Sensors and Transducers, vol. 245, no. 6, pp. 90–98, Oct. 2020.

BibTeX entry:

	@article{quenon_r-testbench_2020-2,
		title = {R-testbench: a {Journey} in {Open} {Source} {Programming} for {Remote} {Instrumentation} with {Python}},
		volume = {245},
		copyright = {All rights reserved},
		issn = {1726-5479},
		language = {english},
		number = {6},
		journal = {Sensors and Transducers},
		author = {Quenon, Alexandre and Daubie, Evelyne and Moeyaert, Véronique and Dualibe, Fortunato},
		month = oct,
		year = {2020},
		pages = {90--98}
	}

BibLaTeX entry:

	@article{quenon_r-testbench_2020-2,
		title = {R-testbench: a Journey in Open Source Programming for Remote Instrumentation with Python},
		volume = {245},
		rights = {All rights reserved},
		issn = {1726-5479},
		shorttitle = {R-testbench},
		pages = {90--98},
		number = {6},
		journaltitle = {Sensors and Transducers},
		author = {Quenon, Alexandre and Daubie, Evelyne and Moeyaert, Véronique and Dualibe, Fortunato},
		date = {2020-10-30}
	}


Another article on R-testbench is:

> A. Quenon, E. Daubie, V. Moeyaert, and F. C. Dualibe, “R-testbench: a Python library for instruments remote control and electronic test bench automation,” in Sensors and Electronic Instrumentation Advances: Proceedings of the 6th International Conference on Sensors and Electronic Instrumentation Advances (SEIA’ 2020) and the 2nd IFSA Frequency & Time Conference (IFTC’ 2020), Porto, Portugal, Sep. 2020, pp. 47–50.


BibTeX entry:

    @inproceedings{quenon_r-testbench_2020-1,
	    author = {Quenon, Alexandre and Daubie, Evelyne and Moeyaert, Véronique and Dualibe, Fortunato Carlos},
	    title = {R-testbench: a {Python} library for instruments remote control and electronic test bench automation},
	    address = {Porto, Portugal},
	    booktitle = {Sensors and {Electronic} {Instrumentation} {Advances}: {Proceedings} of the 6th {International} {Conference} on {Sensors} and {Electronic} {Instrumentation} {Advances} ({SEIA}' 2020) and the 2nd {IFSA} {Frequency} \& {Time} {Conference} ({IFTC}' 2020)},
	    isbn = {978-84-09-23483-7},
	    pages = {47--50},
	    publisher = {IFSA},
	    month = sep,
	    year = {2020}
	}

BibLaTeX entry:

	@inproceedings{quenon_r-testbench_2020-1,
	    author = {Quenon, Alexandre and Daubie, Evelyne and Moeyaert, Véronique and Dualibe, Fortunato Carlos},
	    title = {R-testbench: a Python library for instruments remote control and electronic test bench automation},
	    eventtitle = {Sixth International Conference on Sensors and Electronic Instrumentation Advances ({SEIA}' 2020)},
	    location = {Porto, Portugal},
	    booktitle = {Sensors and Electronic Instrumentation Advances: Proceedings of the 6th International Conference on Sensors and Electronic Instrumentation Advances ({SEIA}' 2020) and the 2nd {IFSA} Frequency \& Time Conference ({IFTC}' 2020)},
	    isbn = {978-84-09-23483-7},
	    pages = {47--50},
	    publisher = {{IFSA}},
	    date = {2020-09-23}
	}
