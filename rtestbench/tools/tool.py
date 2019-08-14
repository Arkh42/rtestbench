
# VISA protocol
import visa

# Scientific computations
import numpy

# Logger
import logging


class Tool:
    """Generic class that defines the features common to all electronic tools."""


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, family=None, brand=None, model=None, serial_num=None):
        """Initialize the generic tool.

        The constructor arguments are necessary to build the _id attribute.
        """
        self.logger = logging.getLogger('rtestbench.tool')
        
        self._family = family
        self._brand = brand
        self._model = model
        self._serial_num = serial_num

        self._id = "{0} {1}/{2} (SN = {3})".format(
            self._brand, self._family, self._model, self._serial_num)

        self._visa_resource = None
        self._data_container = numpy.ndarray

        self._available_transfer_formats = {
            'text':None, 'bin':None, 'bin32': None, 'bin64': None}
        self._transfer_format = None

        self.logger.debug("A(n) {} tool has been created.".format(self._id))


    # Tool's ID
    @property
    def family(self):
        """Returns the tool's family (e.g., oscilloscope, multimeter)."""
        return self._family

    @property
    def brand(self):
        """Returns the tool's brand (e.g., Keysight, Rigol)."""
        return self._brand

    @property
    def model(self):
        """Returns the tool's model (e.g., B2985A)."""
        return self._model

    @property
    def serial_num(self):
        """Returns the tool's serial number."""
        return self._serial_num

    @property
    def id(self):
        """Returns the tool's full ID."""
        return self._id

    
    def __str__(self):
        return "The tool is a(n) {}.".format(self._id)


    # VISA resource management
    ###

    # Time-out
    @property
    def timeout(self):
        return self._visa_resource.timeout

    @timeout.setter
    def timeout(self, time_ms):
        self._visa_resource.timeout = time_ms

    # Data container for queries
    @property
    def data_container(self):
        """Get the data container class (type) used for queries."""
        return self._data_container
    
    @data_container.setter
    def data_container(self, class_name):
        """Set the data container used for queries if and only if the new class name is available for VISA.
        
        Valid classes are (list, tuple, numpy.ndarray).
        """
        if class_name in (list, tuple, numpy.ndarray):
            self._data_container = class_name
        else:
            raise ValueError("Invalid data container type.")

    
    # Formats for data transfer
    def is_available_transfer_format(self, key):
        """Returns True if the passed argument is a transfer format that is available for the tool; False otherwise."""
        if key in self._available_transfer_formats.keys():
            return True
        else:
            return False
    
    def is_implemented_transfer_format(self, key):
        """Returns True is the passed argument is an available transfer format and if the corresponding value is not None; False otherwise."""
        if self.is_available_transfer_format(key) and self._available_transfer_formats[key] is not None:
            return True
        else:
            return False

    @property
    def transfer_format(self):
        """Get the current data transfer format."""
        return self._transfer_format

    @transfer_format.setter
    def transfer_format(self, data_format):
        """Set the data transfer format if and only if the new format is available for the tool."""
        if self.is_available_transfer_format(data_format):
            if self._available_transfer_formats[data_format] is None:
                raise NotImplementedError('The {0} format is available but not implemented for the {1} tool.'.format(data_format, self._id))
            else:
                self._transfer_format = data_format
        else:
            raise ValueError('The {0} format is not available for the {1} tool.\n\
                Valid formats are: {2}'.format(data_format, self._id, self._available_transfer_formats))

    
    # Functions to attach/detach a VISA resource
    def attach_visa_resource(self, visa_resource):
        """Attach a VISA resource to the tool if and only if the session is valid and there is no other resource already attached."""
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
                    self._visa_resource, self._id))
        else:
            raise RuntimeError("A visa resource has already been attached to the {} tool.".format(self._id))

    def detach_visa_resource(self):
        """Detach the current VISA resource from the tool."""
        if self._visa_resource is not None:
            # self.logger.debug("The {0} visa resource is detached from the {1} tool.".format(
            #     self._visa_resource, self._id))
            self._visa_resource.close()
            self._visa_resource = None


    # Sending commands
    ###

    def send(self, command):
        """Send a command which does not expect any return from the tool (e.g., '*RST')."""
        if self._visa_resource is None:
            raise UnboundLocalError("No VISA resource corresponding to the tool.")
        else:
            try:
                self._visa_resource.write(command)
            except visa.VisaIOError as err:
                self.logger.error('VisaIOError: {}'.format(err.description))
                raise RuntimeError("Cannot send the command: {}".format(command))

    def query(self, request):
        """Send a request which expect a return from the tool (e.g., '*IDN?')."""
        if self._visa_resource is None:
            raise UnboundLocalError("No VISA resource corresponding to the tool.")
        try:
            return self._visa_resource.query(request)
        except visa.VisaIOError as err:
            self.logger.error('VisaIOError: {}'.format(err.description))
            raise RuntimeError("Cannot query the request: {}".format(request))       

    def query_data(self, request):
        """Send a request to get data from the tool."""
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
                    raise NotImplementedError("Unsupported data format {} is currently selected.".format(self.transfer_format))
            except visa.VisaIOError as err:
                self.logger.error('VisaIOError: {}'.format(err.description))
                raise RuntimeError("Cannot query the data by requesting: {}".format(request))


    # High-level abstract interface (common to all tools)
    ###

    # Data transfer format
    def config_data_transfer_format(self, data_format):
        """Configure the tool to use the passed format for data transfer.
        
        The transfer_format attribute is set and then the command is sent to the tool.
        """
        raise NotImplementedError('Function not implemented by the Tool class. Must be implemented by daughter classes.')


    # Locks
    def lock(self):
        """Request a remote lock of the tool's I/O interface."""
        raise NotImplementedError('Function not implemented by the Tool class. Must be implemented by daughter classes.')

    def unlock(self):
        """Release the remote lock of the tool's I/O interface."""
        raise NotImplementedError('Function not implemented by the Tool class. Must be implemented by daughter classes.')


    # Reset
    def reset(self):
        """Clears the status registers and reset the tool."""
        self.send('*CLS')
        self.send('*RST')


    # Low-level facilities
    ###

    def is_boolean_string(self, sequence):
        try:
            if sequence.upper() in ('ON', 'OFF', '1', '0'):
                return True
            else:
                return False
        except AttributeError:
            return False
