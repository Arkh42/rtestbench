"""Module that defines the constants used in R-testbench."""


import numpy as np


# Constants for all tools
RTB_DATA_CONTAINERS = (np.ndarray, list, tuple)

RTB_BIN_DATA_ENDIANNESSES = ("big", "little")

RTB_BIN_DATA_HEADERS = ('ieee', 'empty', 'hp')

RTB_BIN_DATA_TYPES_FLOAT = ('f', "float", "bin32")
RTB_BIN_DATA_TYPES_DOUBLE = ('d', "double", "bin64")
RTB_BIN_DATA_TYPES_INT16 = ('h', "short", "int16")
RTB_BIN_DATA_TYPES_INT32 = ('i', 'l', "int", "long", "int32")
RTB_BIN_DATA_TYPES_INT64 = ('q', "long long", "int64")
RTB_BIN_DATA_TYPES_UINT16 = ('H', "unsigned short", "uint16")
RTB_BIN_DATA_TYPES_UINT32 = ('I', 'L', "unsigned int", "unsigned long", "uint32")
RTB_BIN_DATA_TYPES_UINT64 = ('Q', "unsigned long long", "uint64")
RTB_BIN_DATA_TYPES = (
    RTB_BIN_DATA_TYPES_FLOAT,
    RTB_BIN_DATA_TYPES_DOUBLE,
    RTB_BIN_DATA_TYPES_INT16,
    RTB_BIN_DATA_TYPES_INT32,
    RTB_BIN_DATA_TYPES_INT64,
    RTB_BIN_DATA_TYPES_UINT16,
    RTB_BIN_DATA_TYPES_UINT32,
    RTB_BIN_DATA_TYPES_UINT64
)

RTB_TEXT_DATA_CONVERTERS_BIN = ('b', "bin", "binary")
RTB_TEXT_DATA_CONVERTERS_OCT = ('o', "oct", "octal")
RTB_TEXT_DATA_CONVERTERS_HEX = ('x', "hex", "hexadecimal")
RTB_TEXT_DATA_CONVERTERS_DEC = ('d', "dec", "decimal")
RTB_TEXT_DATA_CONVERTERS_FIX = ('f', "fix", "fixed-point")
RTB_TEXT_DATA_CONVERTERS_EXP = ('e', "exp", "exponent")
RTB_TEXT_DATA_CONVERTERS_STR = ('s', "str", "string")
RTB_TEXT_DATA_CONVERTERS = (
    RTB_TEXT_DATA_CONVERTERS_BIN,
    RTB_TEXT_DATA_CONVERTERS_OCT,
    RTB_TEXT_DATA_CONVERTERS_HEX,
    RTB_TEXT_DATA_CONVERTERS_DEC,
    RTB_TEXT_DATA_CONVERTERS_FIX,
    RTB_TEXT_DATA_CONVERTERS_EXP,
    RTB_TEXT_DATA_CONVERTERS_STR
)

RTB_TEXT_DATA_SEPARATORS = (',', ';', ' ')

RTB_TRANSFERT_FORMATS = ("text", "ascii", "bin", "binary")
