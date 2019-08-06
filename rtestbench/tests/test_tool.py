
# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.tool as tool

import logging
import visa
import numpy



class ToolTest(unittest.TestCase):

    """Test case for the Tool class.
    """


    def setUp(self):
        self.default_tool = tool.Tool()
        logging.disable(logging.CRITICAL)
    

    # Useful methods
    ###

    def attach_fake_valid_visa_Resource(self):
        rm = visa.ResourceManager()
        fake_visa_resource = visa.Resource(rm, resource_name='Fake_resource')
        fake_visa_resource.session = 0
        self.default_tool.attach_visa_resource(fake_visa_resource)
    
    def attach_simulated_device(self):
        rm = visa.ResourceManager('@sim')
        sim_visa_resource = rm.open_resource('ASRL1::INSTR')
        self.default_tool.attach_visa_resource(sim_visa_resource)
    
    
    # TEST - initialization & properties
    ###

    def test_default_init(self):
        self.assertIsNone(self.default_tool._family)
        self.assertIsNone(self.default_tool._brand)
        self.assertIsNone(self.default_tool._model)
        self.assertIsNone(self.default_tool._serial_num)
        self.assertIsNone(self.default_tool._visa_resource)
    
    def test_data_container(self):
        # Check default value
        self.assertIs(self.default_tool.data_container, numpy.ndarray)

        # Check valid classes
        self.default_tool.data_container = list
        self.assertIs(self.default_tool.data_container, list)

        self.default_tool.data_container = tuple
        self.assertIs(self.default_tool.data_container, tuple)

        self.default_tool.data_container = numpy.ndarray
        self.assertIs(self.default_tool.data_container, numpy.ndarray)

        # Check invalid classes
        with self.assertRaises(ValueError):
            self.default_tool.data_container = float
    
    def test_transfer_format(self):
        # Check default value
        self.assertIsNone(self.default_tool.transfer_format)

        # Check default data formats (not implemented)
        with self.assertRaises(NotImplementedError):
            self.default_tool.transfer_format = 'text'
            self.default_tool.transfer_format = 'bin'

        # Check invalid data format
        with self.assertRaises(ValueError):
            self.default_tool.transfer_format = 'toto'
        
        # Check newly implemented data format
        self.default_tool._available_transfer_formats.update({'text': 'ascii'})
        self.default_tool.transfer_format = 'text'
        self.assertEqual(self.default_tool.transfer_format, 'text')
    

    # TEST - VISA resource management
    ###

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
        
        # pass a (fake) visa resource object with a (fake) valid session
        fake_visa_resource.session = 0
        self.default_tool.attach_visa_resource(fake_visa_resource)
        self.assertEqual(self.default_tool._visa_resource, fake_visa_resource)

        # pass a valid (fake) visa resource object while another one is alrady attached
        with self.assertRaises(RuntimeError):
            self.default_tool.attach_visa_resource(fake_visa_resource)
    
    def test_detach_visa_resource(self):
        self.attach_fake_valid_visa_Resource()

        self.default_tool.detach_visa_resource()
        self.assertIsNone(self.default_tool._visa_resource)
    

    # TEST - Sending commands
    ###

    def test_send(self):
        # No VISA resource
        with self.assertRaises(UnboundLocalError):
            self.default_tool.send('command')
        
        # Simulated tool
        self.attach_simulated_device()
        self.default_tool.send('command')
    
    def test_query(self):
        # No VISA resource
        with self.assertRaises(UnboundLocalError):
            self.default_tool.query('request')
        
        # No data format
        self.attach_simulated_device()
        with self.assertRaises(UnboundLocalError):
            self.default_tool.query('request')
        
        # Unsupported data formats
        self.default_tool._available_transfer_formats.update({'toto': 'toto'})
        self.default_tool.transfer_format = 'toto'
        with self.assertRaises(RuntimeError):
            self.default_tool.query('request')

        # Valid data formats
        self.default_tool._available_transfer_formats.update({'text': 'ascii'})
        self.default_tool.transfer_format = 'text'
        self.default_tool.query('request')
    

    # TEST - Locks
    ###

    def test_lock_system(self):
        with self.assertRaises(NotImplementedError):
            self.default_tool.lock_system()
    
    def test_unlock_system(self):
        with self.assertRaises(NotImplementedError):
            self.default_tool.unlock_system()
