
# Unit tests framework
import unittest


# Module Under Test
import rtestbench.tools.keysight.electrometer._interface as electrometer

import logging


class KeysightElectrometerTest(unittest.TestCase):

    """Test case for the Keysight Electrometer Interface class."""


    def setUp(self):
        self.default_electrometer = electrometer.Interface(model=None, serial_num=None)
        logging.disable(logging.CRITICAL)
    
    
    def test_default_init(self):
        self.assertEqual(self.default_electrometer._family, 'electrometer')
        self.assertEqual(self.default_electrometer._brand, 'Keysight')

        self.assertIsNone(self.default_electrometer._model)
        self.assertIsNone(self.default_electrometer._serial_num)

        self.assertIsNone(self.default_electrometer._visa_resource)


    def test_is_available_view_mode(self):
        # Not available
        self.assertFalse(self.default_electrometer.is_available_view_mode('toto'))

        # Available
        self.assertTrue(self.default_electrometer.is_available_view_mode('meter'))
        self.assertTrue(self.default_electrometer.is_available_view_mode('roll'))
        self.assertTrue(self.default_electrometer.is_available_view_mode('hist'))
        self.assertTrue(self.default_electrometer.is_available_view_mode('graph'))
    
    def test_view_mode(self):
        # Check default value
        self.assertEqual(self.default_electrometer.view_mode, 'meter')

        # Check valid values
        self.default_electrometer.view_mode = 'roll'
        self.assertEqual(self.default_electrometer.view_mode, 'roll')

        self.default_electrometer.view_mode = 'hist'
        self.assertEqual(self.default_electrometer.view_mode, 'hist')

        self.default_electrometer.view_mode = 'graph'
        self.assertEqual(self.default_electrometer.view_mode, 'graph')

        self.default_electrometer.view_mode = 'meter'
        self.assertEqual(self.default_electrometer.view_mode, 'meter')

        # Check valid values
        with self.assertRaises(ValueError):
            self.default_electrometer.view_mode = 'toto'


    def test_config_data_transfer_format(self):
        # Not available
        with self.assertRaises(RuntimeError):
            self.default_electrometer.config_data_transfer_format('toto')

        # Available formats --> UnboundLocalError thrown because of send() while no VISA resource
        with self.assertRaises(UnboundLocalError):
            self.default_electrometer.config_data_transfer_format('text')
            self.default_electrometer.config_data_transfer_format('bin')
            self.default_electrometer.config_data_transfer_format('bin32')
            self.default_electrometer.config_data_transfer_format('bin64')


    def test_switch_display(self):
        # Invalid values
        with self.assertRaises(ValueError):
            self.default_electrometer.switch_display('ONOFF')
            self.default_electrometer.switch_display(2)
            self.default_electrometer.switch_display(True)

        # Valid values --> RuntimeError thrown after catching UnboundLocalError thrown because no VISA resource
        with self.assertRaises(RuntimeError):
            self.default_electrometer.switch_display('ON')
            self.default_electrometer.switch_display('OFF')
            self.default_electrometer.switch_display('1')
            self.default_electrometer.switch_display('0')
            self.default_electrometer.switch_display(1)
            self.default_electrometer.switch_display(0)


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
