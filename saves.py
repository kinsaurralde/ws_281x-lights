import json
import os

from werkzeug.utils import secure_filename


class Saves():
    def __init__(self):
        self.dir = "saves/"

    def _open_json(self, folder, path):
        file_name = self.dir + folder + '/' + secure_filename(path + ".json")
        save_file = open(file_name, "r")
        return json.load(save_file)

    def _get_json(self, folder, path, data):
        file_data = self._open_json(folder, path)
        return file_data

    def _write_json(self, folder, path, data):
        file_data = self._open_json(folder, path)

    def run_function(self, function, folder, path=None, data=None):
        if function == "list":
            return os.listdir(self.dir + folder + '/')
        elif function == "run":
            file_data = self._get_json(folder, path, data)
            return file_data
        elif function == "write":
            self._write_json(folder, path, data)
            return "Written"
        return "Default Return"
