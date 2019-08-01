
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rtestbench",
    version="0.0.0",
    author="Alexandre Quenon",
    author_email="aquenon@hotmail.be",
    description="A package to create a software remote test bench to control an actual electronic test bench remotely",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arkh42/rtestbench",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
