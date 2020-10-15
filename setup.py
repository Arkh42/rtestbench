
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rtestbench",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'pyvisa >=1.9',
        'pyvisa-py >= 0.3',
        'pyvisa-sim >= 0.4',
        'numpy >=1.13.0',
        'pandas >=0.25.0',
        'matplotlib >=3.0.3',
    ],
    extras_require={
        'hdf5': ['tables >= 3.5.2'],
        'feather': ['feather-format >= 0.4.1'],
    },
    author="Alexandre Quenon",
    author_email="aquenon@hotmail.be",
    description="A package to create a software remote test bench to control an actual electronic test bench remotely",
    long_description=long_description,
    url="https://github.com/Arkh42/rtestbench",
    project_urls={
        "Bug Tracker": "https://github.com/Arkh42/rtestbench/issues",
        "Documentation": "https://github.com/Arkh42/rtestbench",
        "Source Code": "https://github.com/Arkh42/rtestbench",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Electronics",
    ],
)
