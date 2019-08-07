
# Unit tests framework
import unittest


# Module Under Test
import rtestbench.tools.keysight._factory as keysight_factory


class KeysightFactoryTest(unittest.TestCase):

    """Test case for the keysight factory.
    """

    # Electrometers
    def test_b2981a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2981a import B2981A as device

        instr = keysight_factory.find_and_build(model='B2981A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    def test_b2983a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2983a import B2983A as device

        instr = keysight_factory.find_and_build(model='B2983A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    def test_b2985a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2985a import B2985A as device

        instr = keysight_factory.find_and_build(model='B2985A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    def test_b2987a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2987a import B2987A as device

        instr = keysight_factory.find_and_build(model='B2987A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    # Unknown model
    def test_unknown_factory(self):
        with self.assertRaises(ValueError):
            instr = keysight_factory.find_and_build(model='JohnDoe', serial_num=42)



# Module Under Test
import rtestbench.tools._factory as tool_factory


class ToolFactoryTest(unittest.TestCase):

    """Test case for the top-level tool factory.
    """

    # Keysight Electrometers
    def test_keysight_b2981a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2981a import B2981A as device

        instr = tool_factory.find_and_build_tool(brand='Keysight Technologies', model='B2981A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    def test_keysight_b2983a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2983a import B2983A as device

        instr = tool_factory.find_and_build_tool(brand='Keysight Technologies', model='B2983A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    def test_keysight_b2985a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2985a import B2985A as device

        instr = tool_factory.find_and_build_tool(brand='Keysight Technologies', model='B2985A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    def test_keysight_b2987a_factory(self):
        from rtestbench.tools.keysight.electrometer.b2987a import B2987A as device

        instr = tool_factory.find_and_build_tool(brand='Keysight Technologies', model='B2987A', serial_num=42)
        self.assertIsInstance(instr, device)
    
    # Unknown Keysight model
    def test_keysight_unknown_factory(self):
        with self.assertRaises(ValueError):
            instr = tool_factory.find_and_build_tool(brand='Keysight Technologies', model='JohnDoe', serial_num=42)
    
    # Unknown brand
    def test_unknown_factory(self):
        with self.assertRaises(ValueError):
            instr = tool_factory.find_and_build_tool(brand='JohnDoe', model='JohnDoe', serial_num=42)
