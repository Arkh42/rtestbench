
# Unit tests framework
import unittest

# Module Under Test
import rtestbench.tools.tool as tool



class ToolTest(unittest.TestCase):

    """Test case for the Tool class.
    """


    def test_default_init(self):
        default_tool = tool.Tool()

        self.assertIsNone(default_tool._family)
        self.assertIsNone(default_tool._brand)
        self.assertIsNone(default_tool._model)
        self.assertIsNone(default_tool._serial_num)

        self.assertIsNone(default_tool._visa_resource)
