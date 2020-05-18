"""Test for the Keysight electrometer modules."""


import pytest




# Unit tests framework
import unittest


# Module Under Test
import rtestbench.tools.keysight.electrometer._interface_v1 as electrometer

from ._test_facilities import attach_simulated_device_to

import logging
import numpy


class KeysightElectrometerTest(unittest.TestCase):
    """Test case for the Keysight Electrometer Interface class."""


    def setUp(self):
        self.default_electrometer = electrometer.Interface(model=None, serial_num=None)
        logging.disable(logging.CRITICAL)


    # TEST - Initialization & properties
    ###

    # Initialization
    def test_default_init(self):
        # Raw access
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')
        self.assertIsNone(self.default_electrometer._model)
        self.assertIsNone(self.default_electrometer._serial_num)

        self.assertIsNone(self.default_electrometer._visa_resource)
        self.assertIs(self.default_electrometer._data_container, numpy.ndarray)

        self.assertDictEqual(
            self.default_electrometer._available_transfer_formats,
            {'text':'ASCii', 'bin':'REAL,32', 'bin32':'REAL,32', 'bin64':'REAL,64'})
        self.assertIsNone(self.default_electrometer._transfer_format)

        self.assertDictEqual(
            self.default_electrometer._available_meas_data_types,
            {'I': 'CURRent', 'i': 'CURRent'})
        self.assertDictEqual(
            self.default_electrometer._available_result_data_types,
            {'I': 'CURRent', 'i': 'CURRent', 't': 'TIME', 'math': 'MATH'})
        self.assertIsNone(self.default_electrometer._meas_data_type)
        self.assertEqual(self.default_electrometer._result_data_type, list())

        self.assertDictEqual(
            self.default_electrometer._available_view_modes,
            {'meter':'SINGle1', 'roll':'ROLL', 'hist':'HISTogram', 'graph':'GRAPH'})
        self.assertDictEqual(
            self.default_electrometer._available_subview_modes,
            {'roll':'ROLL', 'hist':'HISTogram', 'range':'RANGe', 'trigger': 'TRIGger', 'source': 'FUNCtion'})

        # Getter access
        self.assertEqual(self.default_electrometer.family, 'electrometer')
        self.assertEqual(self.default_electrometer.brand, 'Keysight')
        self.assertIsNone(self.default_electrometer.model)
        self.assertIsNone(self.default_electrometer.serial_num)

        self.assertIs(self.default_electrometer.data_container, numpy.ndarray)

        self.assertIsNone(self.default_electrometer.transfer_format)

        self.assertIsNone(self.default_electrometer.meas_data_type)
        self.assertEqual(self.default_electrometer.result_data_type, list())


    def test_config_defaults(self):
        # Defaults are configured when the tool is attached
        attach_simulated_device_to(self.default_electrometer)

        self.assertEqual(self.default_electrometer.transfer_format, 'text')

        self.assertEqual(self.default_electrometer.view_mode, 'meter')
        self.assertEqual(self.default_electrometer.subview_mode, 'roll')


    # View modes
    def test_is_available_view_mode(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_available_view_mode('toto'))

        # Available
        self.assertTrue(self.default_electrometer.is_available_view_mode('meter'))
        self.assertTrue(self.default_electrometer.is_available_view_mode('roll'))
        self.assertTrue(self.default_electrometer.is_available_view_mode('hist'))
        self.assertTrue(self.default_electrometer.is_available_view_mode('graph'))
    
    def test_is_implemented_view_mode(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_implemented_view_mode('toto'))

        # Available but not implemented
        self.default_electrometer._available_view_modes.update({'toto': None})
        self.assertFalse(self.default_electrometer.is_implemented_view_mode('toto'))

        # Implemented
        self.default_electrometer._available_view_modes.update({'toto': 'Toto'})
        self.assertTrue(self.default_electrometer.is_implemented_view_mode('toto'))

        self.assertTrue(self.default_electrometer.is_implemented_view_mode('meter'))
        self.assertTrue(self.default_electrometer.is_implemented_view_mode('roll'))
        self.assertTrue(self.default_electrometer.is_implemented_view_mode('hist'))
        self.assertTrue(self.default_electrometer.is_implemented_view_mode('graph'))
    
    def test_view_mode(self):
        # Default value
        self.assertIsNone(self.default_electrometer.view_mode)

        # Valid values
        self.default_electrometer.view_mode = 'roll'
        self.assertEqual(self.default_electrometer.view_mode, 'roll')

        self.default_electrometer.view_mode = 'hist'
        self.assertEqual(self.default_electrometer.view_mode, 'hist')

        self.default_electrometer.view_mode = 'graph'
        self.assertEqual(self.default_electrometer.view_mode, 'graph')

        self.default_electrometer.view_mode = 'meter'
        self.assertEqual(self.default_electrometer.view_mode, 'meter')

        # Invalid values
        with self.assertRaises(ValueError):
            self.default_electrometer.view_mode = 'toto'

        # Not implemented
        self.default_electrometer._available_view_modes.update({'toto': None})
        with self.assertRaises(NotImplementedError):
            self.default_electrometer.view_mode = 'toto'


    def test_is_available_subview_mode(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_available_subview_mode('toto'))

        # Available
        self.assertTrue(self.default_electrometer.is_available_subview_mode('roll'))
        self.assertTrue(self.default_electrometer.is_available_subview_mode('hist'))
        self.assertTrue(self.default_electrometer.is_available_subview_mode('range'))
        self.assertTrue(self.default_electrometer.is_available_subview_mode('trigger'))
        self.assertTrue(self.default_electrometer.is_available_subview_mode('source'))

    def test_is_implemented_subview_mode(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_implemented_subview_mode('toto'))

        # Available but not implemented
        self.default_electrometer._available_subview_modes.update({'toto': None})
        self.assertFalse(self.default_electrometer.is_implemented_subview_mode('toto'))

        # Implemented
        self.default_electrometer._available_subview_modes.update({'toto': 'Toto'})
        self.assertTrue(self.default_electrometer.is_implemented_subview_mode('toto'))

        self.assertTrue(self.default_electrometer.is_implemented_subview_mode('roll'))
        self.assertTrue(self.default_electrometer.is_implemented_subview_mode('hist'))
        self.assertTrue(self.default_electrometer.is_implemented_subview_mode('range'))
        self.assertTrue(self.default_electrometer.is_implemented_subview_mode('trigger'))
        self.assertTrue(self.default_electrometer.is_implemented_subview_mode('source'))

    def test_subview_mode(self):
        # Check default value
        self.assertIsNone(self.default_electrometer.subview_mode)

        # Check valid values
        self.default_electrometer.subview_mode = 'hist'
        self.assertEqual(self.default_electrometer.subview_mode, 'hist')

        self.default_electrometer.subview_mode = 'range'
        self.assertEqual(self.default_electrometer.subview_mode, 'range')

        self.default_electrometer.subview_mode = 'trigger'
        self.assertEqual(self.default_electrometer.subview_mode, 'trigger')

        self.default_electrometer.subview_mode = 'source'
        self.assertEqual(self.default_electrometer.subview_mode, 'source')

        self.default_electrometer.subview_mode = 'roll'
        self.assertEqual(self.default_electrometer.subview_mode, 'roll')

        # Check invalid values
        with self.assertRaises(ValueError):
            self.default_electrometer.subview_mode = 'toto'

        # Not implemented
        self.default_electrometer._available_subview_modes.update({'toto': None})
        with self.assertRaises(NotImplementedError):
            self.default_electrometer.subview_mode = 'toto'


    # TEST - High-level abstract interface (common to all tools)
    ###

    def test_config_data_transfer_format(self):
        # Not available
        with self.assertRaises(RuntimeError):
            self.default_electrometer.config_data_transfer_format('toto')

        # Available formats
        attach_simulated_device_to(self.default_electrometer)

        self.default_electrometer.config_data_transfer_format('text')
        self.default_electrometer.config_data_transfer_format('bin')
        self.default_electrometer.config_data_transfer_format('bin32')
        self.default_electrometer.config_data_transfer_format('bin64')
    
    
    # TEST - Display
    ###

    def test_switch_display(self):
        # Invalid values
        with self.assertRaises(ValueError):
            self.default_electrometer.switch_display('ONOFF')
            self.default_electrometer.switch_display(2)
            self.default_electrometer.switch_display(True)
            self.default_electrometer.switch_display(False)

        # Valid values
        attach_simulated_device_to(self.default_electrometer)

        self.default_electrometer.switch_display('ON')
        self.default_electrometer.switch_display('OFF')
        self.default_electrometer.switch_display('1')
        self.default_electrometer.switch_display('0')
        self.default_electrometer.switch_display(1)
        self.default_electrometer.switch_display(0)


    # Measurements conditions
    ###

    def test_switch_autorange(self):
        # No measurement data type selected
        with self.assertRaises(RuntimeError):
            self.default_electrometer.switch_autorange('ON')

        # Invalid values
        self.default_electrometer.meas_data_type = 'I'
        with self.assertRaises(ValueError):
            self.default_electrometer.switch_display('ONOFF')
            self.default_electrometer.switch_display(2)
            self.default_electrometer.switch_display(True)
            self.default_electrometer.switch_display(False)

        # Valid values
        attach_simulated_device_to(self.default_electrometer)

        self.default_electrometer.switch_autorange('ON')
        self.default_electrometer.switch_autorange('OFF')
        self.default_electrometer.switch_autorange('1')
        self.default_electrometer.switch_autorange('0')
        self.default_electrometer.switch_autorange('on')
        self.default_electrometer.switch_autorange('off')
        self.default_electrometer.switch_autorange(1)
        self.default_electrometer.switch_autorange(0)
    
    def test_config_range(self):
        # No measurement data type selected
        with self.assertRaises(RuntimeError):
            self.default_electrometer.config_range(1e-3)

        # Valid values
        self.default_electrometer.meas_data_type = 'I'
        attach_simulated_device_to(self.default_electrometer)

        self.default_electrometer.config_range(1e-3)
    
    def test_config_aperture_time(self):
        # No measurement data type selected
        with self.assertRaises(RuntimeError):
            self.default_electrometer.config_aperture_time(1e-3)

        # Valid values
        self.default_electrometer.meas_data_type = 'I'
        attach_simulated_device_to(self.default_electrometer)

        self.default_electrometer.config_aperture_time(1e-3)


# Module Under Test
import rtestbench.tools.keysight.electrometer.b2981a as b2981a


class KeysightB2981ATest(unittest.TestCase):

    """Test case for the Keysight Electrometer B2981A class."""


    def setUp(self):
        self.default_electrometer = b2981a.B2981A(serial_num=42)
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')
        self.assertEqual(self.default_electrometer._model, 'B2981A')
        self.assertEqual(self.default_electrometer._serial_num, 42)

        self.assertIsNone(self.default_electrometer._visa_resource)



# Module Under Test
import rtestbench.tools.keysight.electrometer.b2983a as b2983a


class KeysightB2983ATest(unittest.TestCase):

    """Test case for the Keysight Electrometer B2983A class."""


    def setUp(self):
        self.default_electrometer = b2983a.B2983A(serial_num=42)
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')
        self.assertEqual(self.default_electrometer._model, 'B2983A')
        self.assertEqual(self.default_electrometer._serial_num, 42)

        self.assertIsNone(self.default_electrometer._visa_resource)



# Module Under Test
import rtestbench.tools.keysight.electrometer.b2985a as b2985a


class KeysightB2985ATest(unittest.TestCase):

    """Test case for the Keysight Electrometer B2985A class."""


    def setUp(self):
        self.default_electrometer = b2985a.B2985A(serial_num=42)
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')
        self.assertEqual(self.default_electrometer._model, 'B2985A')
        self.assertEqual(self.default_electrometer._serial_num, 42)

        self.assertIsNone(self.default_electrometer._visa_resource)

        self.assertDictEqual(
            self.default_electrometer._available_output_off_cond,
            {'default': 'NORMal', 'normal': 'NORMal',
            'hiz': 'HIZ', 'HiZ': 'HIZ', 'HIZ': 'HIZ',
            'zero': 'ZERO', 0:'ZERO', '0':'ZERO'})



# Module Under Test
import rtestbench.tools.keysight.electrometer.b2987a as b2987a


class KeysightB2987ATest(unittest.TestCase):

    """Test case for the Keysight Electrometer B2987A class."""


    def setUp(self):
        self.default_electrometer = b2987a.B2987A(serial_num=42)
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')
        self.assertEqual(self.default_electrometer._model, 'B2987A')
        self.assertEqual(self.default_electrometer._serial_num, 42)

        self.assertIsNone(self.default_electrometer._visa_resource)
