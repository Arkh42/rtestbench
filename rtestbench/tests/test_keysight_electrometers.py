
# Unit tests framework
import unittest


# Module Under Test
import rtestbench.tools.keysight.electrometer._interface as electrometer


class KeysightElectrometerTest(unittest.TestCase):

    """Test case for the Keysight Electrometer Interface class."""


    def setUp(self):
        self.default_electrometer = electrometer.Interface(model=None, serial_num=None)
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')

        self.assertIsNone(self.default_electrometer._model)
        self.assertIsNone(self.default_electrometer._serial_num)

        self.assertIsNone(self.default_electrometer._visa_resource)



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
