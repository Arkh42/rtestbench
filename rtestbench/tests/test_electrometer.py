
# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.electrometer as electrometer



class ElectrometerTest(unittest.TestCase):

    """Test case for the Electrometer class.
    """


    def test_default_init(self):
        default_electrometer = electrometer.Electrometer()

        self.assertEqual(default_electrometer._family, 'electrometer')

        self.assertIsNone(default_electrometer._brand)
        self.assertIsNone(default_electrometer._model)
        self.assertIsNone(default_electrometer._serial_num)

        self.assertIsNone(default_electrometer._visa_resource)
