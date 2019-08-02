
# VISA protocol
import visa

# Logger
import logging


class Tool:

    """Generic class that defines the features common to all electronic tools.
    """


    def __init__(self, family=None, brand=None, model=None, serial_num=None):

        """Initialize the generic tool.

        The constructor arguments are necessary to build the _system_id attribute
        """

        self.logger = logging.getLogger('rtestbench.tool')
        
        self._family = family

        self._brand = brand
        self._model = model
        self._serial_num = serial_num

        self._id = "{0} {1}/{2} (SN = {3})".format(
            self._brand, self._family, self._model, self._serial_num
        )

        self._visa_resource = None

        self.logger.debug("A(n) {} tool is created.".format(self._id))
    

    def __str__(self):
        return "The tool is a(n) {}.".format(self._id)
    

    def attach_visa_resource(self, visa_resource):
        if self._visa_resource is None:
            try:
                visa_resource.session
            except AttributeError:
                raise TypeError("The passed visa_resource argument is not a visa Resource object.")
            except visa.InvalidSession as error_msg:
                raise RuntimeError(error_msg)
            else:
                self._visa_resource = visa_resource
                self.logger.debug("The {0} visa resource is attached to the {1} tool.".format(
                    self._visa_resource, self._id
                ))
        else:
            raise RuntimeError("A visa resource has already been attached to the {} tool.".format(self._id))
    
    def detach_visa_resource(self):
        if self._visa_resource is not None:
            self.logger.debug("The {0} visa resource is detached from the {1} tool.".format(
                self._visa_resource, self._id
            ))
            self._visa_resource.close()
            self._visa_resource = None
