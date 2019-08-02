
# Unit tests framework
import unittest

# Package Under Test
import rtestbench



class RTestBenchTest(unittest.TestCase):

    """Test case for the RTestBench class
    """


    def setUp(self):
        self.rtb = rtestbench.RTestBench(verbose=False)


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



if __name__ == "__main__":
    unittest.main()
