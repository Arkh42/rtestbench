"""Test for the core module."""


import pytest





#TODO: update to the new Tool architecture and with pytest

# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.electrometer_v1 as electrometer

import numpy



class ElectrometerTest(unittest.TestCase):
    """Test case for the Electrometer class."""


    def setUp(self):
        self.default_electrometer = electrometer.Electrometer_v1()


    # TEST - Initialization & properties
    ###

    # Initialization
    def test_default_init(self):
        # Raw access
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertIsNone(self.default_electrometer._brand)
        self.assertIsNone(self.default_electrometer._model)
        self.assertIsNone(self.default_electrometer._serial_num)

        self.assertIsNone(self.default_electrometer._visa_resource)
        self.assertIs(self.default_electrometer._data_container, numpy.ndarray)

        self.assertDictEqual(
            self.default_electrometer._available_transfer_formats,
            {'text':None, 'bin':None, 'bin32': None, 'bin64': None})
        self.assertIsNone(self.default_electrometer._transfer_format)

        self.assertEqual(self.default_electrometer._available_meas_data_types, dict())
        self.assertEqual(self.default_electrometer._available_result_data_types, dict())

        self.assertIsNone(self.default_electrometer._meas_data_type)
        self.assertEqual(self.default_electrometer._result_data_type, list())

        self.assertEqual(self.default_electrometer._available_trigger_sources, dict())
        self.assertIsNone(self.default_electrometer._trigger_source)

        # Getter access
        self.assertEqual(self.default_electrometer.family, 'electrometer')
        self.assertIsNone(self.default_electrometer.brand)
        self.assertIsNone(self.default_electrometer.model)
        self.assertIsNone(self.default_electrometer.serial_num)

        self.assertIs(self.default_electrometer.data_container, numpy.ndarray)

        self.assertIsNone(self.default_electrometer.transfer_format)

        self.assertIsNone(self.default_electrometer.meas_data_type)
        self.assertEqual(self.default_electrometer.result_data_type, list())

        self.assertIsNone(self.default_electrometer.trigger_source)


    # Data types for results and measurements
    def test_is_available_meas_data_type(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_available_meas_data_type('toto'))

        # Available
        self.default_electrometer._available_meas_data_types.update({'toto': None})
        self.assertTrue(self.default_electrometer.is_available_meas_data_type('toto'))

    def test_is_implemented_meas_data_type(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_implemented_meas_data_type('toto'))

        # Available but not implemented
        self.default_electrometer._available_meas_data_types.update({'toto': None})
        self.assertFalse(self.default_electrometer.is_implemented_meas_data_type('toto'))

        # Implemented
        self.default_electrometer._available_meas_data_types.update({'toto': 'Toto'})
        self.assertTrue(self.default_electrometer.is_implemented_meas_data_type('toto'))

    def test_is_available_result_data_type(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_available_result_data_type('toto'))

        # Available
        self.default_electrometer._available_result_data_types.update({'toto': None})
        self.assertTrue(self.default_electrometer.is_available_result_data_type('toto'))
    
    def test_is_implemented_result_data_type(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_implemented_result_data_type('toto'))

        # Available but not implemented
        self.default_electrometer._available_result_data_types.update({'toto': None})
        self.assertFalse(self.default_electrometer.is_implemented_result_data_type('toto'))

        # Implemented
        self.default_electrometer._available_result_data_types.update({'toto': 'Toto'})
        self.assertTrue(self.default_electrometer.is_implemented_result_data_type('toto'))
    
    def test_meas_data_type(self):
        # Default value
        self.assertIsNone(self.default_electrometer.meas_data_type)

        # Invalid data format
        with self.assertRaises(ValueError):
            self.default_electrometer.meas_data_type = 'toto'
        
        # Not implemented
        self.default_electrometer._available_meas_data_types.update({'toto': None})
        with self.assertRaises(NotImplementedError):
            self.default_electrometer.meas_data_type = 'toto'
        
        # Implemented data format
        self.default_electrometer._available_meas_data_types.update({'I': 'current'})
        self.default_electrometer.meas_data_type = 'I'
        self.assertEqual(self.default_electrometer.meas_data_type, 'I')

    def test_result_data_type(self):
        # Default value
        self.assertEqual(self.default_electrometer.result_data_type, list())

        # Invalid data format
        with self.assertRaises(ValueError):
            self.default_electrometer.result_data_type = ['toto']
        
        # Not implemented
        self.default_electrometer._available_result_data_types.update({'toto': None})
        with self.assertRaises(NotImplementedError):
            self.default_electrometer.result_data_type = ['toto']
        
        # Implemented data format
        self.default_electrometer._available_result_data_types.update({'I': 'current'})
        self.default_electrometer.result_data_type = ['I']
        self.assertEqual(self.default_electrometer.result_data_type, ['I'])
    

    # Trigger sources
    def test_is_available_trigger_source(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_available_trigger_source('toto'))

        # Available
        self.default_electrometer._available_trigger_sources.update({'toto': None})
        self.assertTrue(self.default_electrometer.is_available_trigger_source('toto'))
    
    def test_trigger_source(self):
        # Default value
        self.assertEqual(self.default_electrometer.trigger_source, None)

        # Invalid source
        with self.assertRaises(ValueError):
            self.default_electrometer.trigger_source = 'toto'
        
        # Not implemented
        self.default_electrometer._available_trigger_sources.update({'toto': None})
        with self.assertRaises(NotImplementedError):
            self.default_electrometer.trigger_source = 'toto'
        
        # Implemented data format
        self.default_electrometer._available_trigger_sources.update({'timer': 'TIMer'})
        self.default_electrometer.trigger_source = 'timer'
        self.assertEqual(self.default_electrometer.trigger_source, 'timer')


    # TEST - High-level abstract interface
    ###

    def test_abstract_interface(self):
        with self.assertRaises(NotImplementedError):
            # Enable/disable
            self.default_electrometer.switch_display('ON')
            self.default_electrometer.enable_display()
            self.default_electrometer.disable_display()

            # View mode
            self.default_electrometer.config_display_view('mode')

            # Scale and offset
            self.default_electrometer.config_scale('axis', 'scale')
            self.default_electrometer.config_offset('axis', 'offset')
            self.default_electrometer.config_xscale('scale')
            self.default_electrometer.config_xoffset('offset')
            self.default_electrometer.config_yscale('scale')
            self.default_electrometer.config_yoffset('offset')

            # Data type
            self.config_result_data_type('I')
            
            # Range
            self.default_electrometer.switch_autorange('ON')
            self.default_electrometer.enable_autorange()
            self.default_electrometer.disable_autorange()
            self.default_electrometer.config_range('value')

            # Aperture/integration time
            self.default_electrometer.config_aperture_time('value')
            self.default_electrometer.config_aperture_time_min()
            self.default_electrometer.config_aperture_time_max()

            # Trigger
            self.default_electrometer.config_trigger_count('value')
            self.default_electrometer.config_trigger_count_min()
            self.default_electrometer.config_trigger_count_max()

            self.default_electrometer.config_trigger_timer('value')
            self.default_electrometer.config_trigger_timer_min()
            self.default_electrometer.config_trigger_timer_max()

            # Measurements operations
            self.default_electrometer.init_meas()
            self.default_electrometer.fetch_data('data_label')
