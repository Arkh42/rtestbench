"""Module dedicated to the control of the Keysight electrometers B298x series."""


from rtestbench.core import ToolInfo
from rtestbench.tools.electrometer import Electrometer


class B298X(Electrometer):
    """Interface common to all electrometers from the Keysight B298X series.
    """

    def __init__(self, info: ToolInfo):
        Electrometer.__init__(self, info)

        # self._properties.transfer_formats = 
    

    # Common SCPI commands
    def lock(self):
        """Requests a remote lock of the tool's I/O interface."""

        raise NotImplementedError("This function must be implemented by daughter classes.")

    def unlock(self):
        """Releases the remote lock of the tool's I/O interface."""

        try:
            self.send(":SYSTem:LOCK:RELease")
        except IOError:
            raise


    # Scale and offset interface
    def set_scale(self, axis, scale):
        pass

    # Range interface


    # Aperture (integration) time interface

