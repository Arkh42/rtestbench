
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
