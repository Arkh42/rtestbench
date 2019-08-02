
# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.electrometer as electrometer



class ElectrometerTest(unittest.TestCase):

    """Test case for the Electrometer class.
    """


    def setUp(self):
        self.default_electrometer = electrometer.Electrometer()
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')

        self.assertIsNone(self.default_electrometer._brand)
        self.assertIsNone(self.default_electrometer._model)
        self.assertIsNone(self.default_electrometer._serial_num)

        self.assertIsNone(self.default_electrometer._visa_resource)
