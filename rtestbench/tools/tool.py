
import visa


class Tool:

    """Generic class that defines the features common to all electronic tools.
    """


    def __init__(self, family=None, brand=None, model=None, serial_num=None):

        """Initialize the generic tool.

        The constructor arguments are necessary to build the _system_id attribute
        """

        self._family = family

        self._brand = brand
        self._model = model
        self._serial_num = serial_num

        self._id = "{0} {1}/{2} (SN = {3})".format(
            self._brand, self._family, self._model, self._serial_num
        )

        self._visa_resource = None
    

    def __str__(self):
        return "The tool is a(n) {}.".format(self._id)
