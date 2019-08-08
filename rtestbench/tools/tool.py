
# VISA protocol
import visa

# Scientific computations
import numpy

# Logger
import logging


class Tool:

    """Generic class that defines the features common to all electronic tools.
    """


    # Initialization & properties
    ###

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
        self._data_container = numpy.ndarray

        self._available_transfer_formats = {
            'text':None, 'bin':None, 'bin32': None, 'bin64': None
        }
        self._transfer_format = None

        self.logger.debug("A(n) {} tool has been created.".format(self._id))
    

    @property
    def data_container(self):
        """Get data container type."""

        return self._data_container
    
    @data_container.setter
    def data_container(self, class_name):
        """Set data_container. Valid types are (list, tuple, numpy.ndarray).
        """

        if class_name in (list, tuple, numpy.ndarray):
            self._data_container = class_name
        else:
            raise ValueError("Invalid data container type.")
    

    
    def is_available_transfer_format(self, key):
        if key in self._available_transfer_formats.keys():
            return True
        else:
            return False
    
    def is_implemented_transfer_format(self, key):
        if self.is_available_transfer_format(key) and self._available_transfer_formats[key] is not None:
            return True
        else:
            return False

    @property
    def transfer_format(self):
        """Get data transfer format."""

        return self._transfer_format

    @transfer_format.setter
    def transfer_format(self, data_format):
        """Set data transfer format."""

        if self.is_available_transfer_format(data_format):
            if self._available_transfer_formats[data_format] is None:
                raise NotImplementedError('The {0} format is available but not implemented for the {1} tool.'.format(data_format, self._id))
            else:
                self._transfer_format = data_format
        else:
            raise ValueError('The {0} format is not available for the {1} tool.'.format(data_format, self._id))

    
    
    def __str__(self):
        return "The tool is a(n) {}.".format(self._id)
    

    # VISA resource management
    ###

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
            # self.logger.debug("The {0} visa resource is detached from the {1} tool.".format(
            #     self._visa_resource, self._id
            # ))
            self._visa_resource.close()
            self._visa_resource = None
    

    # Sending commands
    ###

    def send(self, command):
        if self._visa_resource is None:
            raise UnboundLocalError("No VISA resource corresponding to the tool.")
        else:
            try:
                self._visa_resource.write(command)
            except visa.VisaIOError as error:
                self.logger.error('VisaIOError:', error.args)
                raise RuntimeError("Cannot send the command: {}".format(command))
    
    def query(self, request):
        if self._visa_resource is None:
            raise UnboundLocalError("No VISA resource corresponding to the tool.")
        try:
            return self._visa_resource.query(request)
        except visa.VisaIOError as err:
            self.logger.error('VisaIOError:', err.args)
            raise RuntimeError("Cannot query the request {}!".format(request))       
    
    def query_data(self, request):
        if self._visa_resource is None:
            raise UnboundLocalError("No VISA resource corresponding to the tool.")
        elif self.transfer_format is None:
            raise UnboundLocalError("No data format is selected for the tool.")
        else:
            try:
                if self.transfer_format is 'text':
                    return self._visa_resource.query_ascii_values(request, container=self.data_container)
                elif self.transfer_format in ('bin', 'bin32'):
                    return self._visa_resource.query_binary_values(request, datatype='f', container=self.data_container)
                elif self.transfer_format is 'bin64':
                    return self._visa_resource.query_binary_values(request, datatype='d', container=self.data_container)
                else:
                    raise RuntimeError("Unsupported data format")
            except RuntimeError as err:
                self.logger.error(err)
                raise RuntimeError("Cannot query the data by requesting {}!".format(request))
            except visa.VisaIOError as err:
                self.logger.error('VisaIOError:', err.args)
                raise RuntimeError("Cannot query the data by requesting {}!".format(request))
    

    # High-level abstract interface (common to all tools)
    ###

    def config_data_transfer_format(self, data_format):
        raise NotImplementedError('Function not implemented by the Tool class. Must be implemented by daughter classes.')

    
    def lock_system(self):
        raise NotImplementedError('Function not implemented by the Tool class. Must be implemented by daughter classes.')
    
    def unlock_system(self):
        raise NotImplementedError('Function not implemented by the Tool class. Must be implemented by daughter classes.')
