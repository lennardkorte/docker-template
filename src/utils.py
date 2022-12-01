
import json

from pathlib import Path
from collections import OrderedDict


class Utils():

    @staticmethod
    def read_json(file_name):
        file_name = Path(file_name)
        with file_name.open('rt') as handle:
            return json.load(handle, object_hook=OrderedDict)

    @staticmethod
    def write_json(content, file_name):
        file_name = Path(file_name)
        with file_name.open('wt') as handle:
            json.dump(content, handle, indent=4, sort_keys=False)