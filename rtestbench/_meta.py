"""A meta-data utility.

Relies on the json module.
Writes files from information sent by rtestbench.
TO BE IMPLEMENTED - Allows to configure a test bench by loading a config file.
"""



import json
from pathlib import Path
from datetime import (datetime, timezone)



class MetaDataManager(object):

    """Manager for meta-data.
    
    Attributes:
        _file_path: A pathlib.Path object describing the path to the meta-data file.
        _file_stream: A file object to stream meta-data to a json file.
    """


    def __init__(self, file_path):
        self._file_path = Path(file_path)
        self._file_path = file_path.with_suffix(".meta.json")

        self._file_stream = open(self._file_path, 'w')
    

    def __del__(self):
        self._file_stream.close()
    

    # Generic functions
    def dump_meta(self, metadata: dict):
        json.dump(metadata, self._file_stream)
    
    def dump_timestamp(self, label: str):
        timestamp = datetime.now(tz=timezone.utc).astimezone().isoformat()
        metadata = {label:timestamp}
        self.dump_meta(metadata)
    

    # Specific functions
