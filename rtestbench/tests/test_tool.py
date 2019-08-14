
# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.tool as tool

from ._test_facilities import attach_simulated_device_to

import logging
import visa
import numpy



class ToolTest(unittest.TestCase):
    """Test case for the Tool class. """


    def setUp(self):
        self.default_tool = tool.Tool()
        logging.disable(logging.CRITICAL)


    # TEST - Initialization & properties
    ###

    def test_default_init(self):
        # Raw access
        self.assertIsNone(self.default_tool._family)
        self.assertIsNone(self.default_tool._brand)
        self.assertIsNone(self.default_tool._model)
        self.assertIsNone(self.default_tool._serial_num)
        self.assertIsInstance(self.default_tool._id, str)

        self.assertIsNone(self.default_tool._visa_resource)
        self.assertIs(self.default_tool._data_container, numpy.ndarray)

        self.assertDictEqual(
            self.default_tool._available_transfer_formats,
            {'text':None, 'bin':None, 'bin32': None, 'bin64': None})
        self.assertIsNone(self.default_tool._transfer_format)

        # Getter access
        self.assertIsNone(self.default_tool.family)
        self.assertIsNone(self.default_tool.brand)
        self.assertIsNone(self.default_tool.model)
        self.assertIsNone(self.default_tool.serial_num)
        self.assertIsInstance(self.default_tool.id, str)

        self.assertIs(self.default_tool.data_container, numpy.ndarray)

        self.assertIsNone(self.default_tool.transfer_format)


    # TEST - VISA resource management
    ###

    # Data container for queries
    def test_data_container(self):
        # Default value
        self.assertIs(self.default_tool.data_container, numpy.ndarray)

        # Valid classes
        self.default_tool.data_container = list
        self.assertIs(self.default_tool.data_container, list)

        self.default_tool.data_container = tuple
        self.assertIs(self.default_tool.data_container, tuple)

        self.default_tool.data_container = numpy.ndarray
        self.assertIs(self.default_tool.data_container, numpy.ndarray)

        # Invalid classes
        with self.assertRaises(ValueError):
            self.default_tool.data_container = float
            self.default_tool.data_container = int
            self.default_tool.data_container = str


    # Formats for data transfer
    def test_is_available_transfer_format(self):
        # Not available
        self.assertFalse(self.default_tool.is_available_transfer_format('toto'))

        # Available
        self.default_tool._available_transfer_formats.update({'toto': None})
        self.assertTrue(self.default_tool.is_available_transfer_format('toto'))

    def test_is_implemented_transfer_format(self):
        # Not available
        self.assertFalse(self.default_tool.is_implemented_transfer_format('toto'))

        # Available but not implemented
        self.default_tool._available_transfer_formats.update({'toto': None})
        self.assertFalse(self.default_tool.is_implemented_transfer_format('toto'))

        # Implemented
        self.default_tool._available_transfer_formats.update({'toto': 'Toto'})
        self.assertTrue(self.default_tool.is_implemented_transfer_format('toto'))

    def test_transfer_format(self):
        # Default value
        self.assertIsNone(self.default_tool.transfer_format)

        # Default data formats (not implemented)
        with self.assertRaises(NotImplementedError):
            self.default_tool.transfer_format = 'text'
            self.default_tool.transfer_format = 'bin'

        # Invalid data format
        with self.assertRaises(ValueError):
            self.default_tool.transfer_format = 'toto'
        
        # Implemented data format
        self.default_tool._available_transfer_formats.update({'text': 'ascii'})
        self.default_tool.transfer_format = 'text'
        self.assertEqual(self.default_tool.transfer_format, 'text')
    

    # Functions to attach/detach a VISA resource
    def test_attach_visa_resource(self):
        # pass a non visa resource object
        with self.assertRaises(TypeError):
            self.default_tool.attach_visa_resource('Wrong_resource')
            self.default_tool.attach_visa_resource(42)
        
        # pass a (fake) visa resource object with invalid session
        rm = visa.ResourceManager()
        fake_visa_resource = visa.Resource(rm, 'Fake_resource')
        with self.assertRaises(RuntimeError):
            self.default_tool.attach_visa_resource(fake_visa_resource)
        rm.close()
        
        # pass a (simulated) visa resource object with a valid session
        rm = visa.ResourceManager('@sim')
        sim_visa_resource = rm.open_resource('ASRL1::INSTR')
        self.default_tool.attach_visa_resource(sim_visa_resource)
        self.assertEqual(self.default_tool._visa_resource, sim_visa_resource)

        # pass a (simulated) visa resource object while another one is already attached
        with self.assertRaises(RuntimeError):
            self.default_tool.attach_visa_resource(sim_visa_resource)
    
    def test_detach_visa_resource(self):
        attach_simulated_device_to(self.default_tool)
        self.assertIsNotNone(self.default_tool._visa_resource)

        self.default_tool.detach_visa_resource()
        self.assertIsNone(self.default_tool._visa_resource)
    

    # TEST - Sending commands
    ###

    def test_send(self):
        # No VISA resource
        with self.assertRaises(UnboundLocalError):
            self.default_tool.send('command')
        
        # Simulated tool
        attach_simulated_device_to(self.default_tool)
        # self.attach_simulated_device()
        self.default_tool.send('command')
    
    def test_query(self):
        # No VISA resource
        with self.assertRaises(UnboundLocalError):
            self.default_tool.query_data('request')
        
        # Valid request
        attach_simulated_device_to(self.default_tool)
        self.default_tool.query('request')
    
    def test_query_data(self):
        # No VISA resource
        with self.assertRaises(UnboundLocalError):
            self.default_tool.query_data('request')
        
        # No data format
        attach_simulated_device_to(self.default_tool)
        with self.assertRaises(UnboundLocalError):
            self.default_tool.query_data('request')
        
        # Unsupported data format
        self.default_tool._available_transfer_formats.update({'toto': 'toto'})
        self.default_tool.transfer_format = 'toto'
        with self.assertRaises(NotImplementedError):
            self.default_tool.query_data('request')

        # Valid data format
        self.default_tool._available_transfer_formats.update({'text': 'ascii'})
        self.default_tool.transfer_format = 'text'
        self.default_tool.query_data('request')
    

    # TEST - High-level abstract interface
    ###

    def test_abstract_interface(self):
        attach_simulated_device_to(self.default_tool)

        with self.assertRaises(NotImplementedError):

            # Data transfer format
            self.default_tool.config_data_transfer_format('text')

            # Locks
            self.default_tool.lock()
            self.default_tool.unlock()
        
        self.default_tool.reset()


    # TEST - Low-level facilities
    ###

    def test_is_boolean_string(self):
        # Boolean strings
        self.assertTrue(self.default_tool.is_boolean_string('ON'))
        self.assertTrue(self.default_tool.is_boolean_string('OFF'))
        self.assertTrue(self.default_tool.is_boolean_string('on'))
        self.assertTrue(self.default_tool.is_boolean_string('off'))
        self.assertTrue(self.default_tool.is_boolean_string('1'))
        self.assertTrue(self.default_tool.is_boolean_string('0'))

        # Non boolean strings
        self.assertFalse(self.default_tool.is_boolean_string('42'))
        self.assertFalse(self.default_tool.is_boolean_string('toto'))

        # Non strings
        self.assertFalse(self.default_tool.is_boolean_string(1))
        self.assertFalse(self.default_tool.is_boolean_string(0))
