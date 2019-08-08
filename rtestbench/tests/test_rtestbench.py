
# Unit tests framework
import unittest

# Package Under Test
import rtestbench

import logging
import visa


class RTestBenchTest(unittest.TestCase):

    """Test case for the RTestBench class.
    """


    def setUp(self):
        self.rtb = rtestbench.RTestBench(verbose=False)
        logging.disable(logging.CRITICAL)


    def test_say_welcome(self):
        message = self.rtb.say_welcome()
        self.assertIsInstance(message, str)
    
    def test_say_goodbye(self):
        message = self.rtb.say_goodbye()
        self.assertIsInstance(message, str)
    
    def test_say_ready(self):
        message = self.rtb.say_ready()
        self.assertIsInstance(message, str)


    def test_detect_resources(self):
        detected_resources = self.rtb.detect_resources()
        self.assertIsInstance(detected_resources, tuple)
    
    def test_attach_resource(self):
        # Simulated resource: not implemented
        rm = visa.ResourceManager('@sim')
        with self.assertRaises(ValueError):
            self.rtb.attach_resource('ASRL1::INSTR')



if __name__ == "__main__":
    unittest.main()
