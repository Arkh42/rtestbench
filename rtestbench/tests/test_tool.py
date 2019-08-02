
# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.tool as tool
import visa



class ToolTest(unittest.TestCase):

    """Test case for the Tool class.
    """


    def setUp(self):
        self.default_tool = tool.Tool()
    
    
    def test_default_init(self):
        self.assertIsNone(self.default_tool._family)
        self.assertIsNone(self.default_tool._brand)
        self.assertIsNone(self.default_tool._model)
        self.assertIsNone(self.default_tool._serial_num)
        self.assertIsNone(self.default_tool._visa_resource)
    

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
        # pass a valid (fake) visa resource
        rm = visa.ResourceManager()
        fake_visa_resource = visa.Resource(rm, 'Fake_resource')
        fake_visa_resource.session = 0
        self.default_tool.attach_visa_resource(fake_visa_resource)

        self.default_tool.detach_visa_resource()
        self.assertIsNone(self.default_tool._visa_resource)
