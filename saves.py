import json

from werkzeug.utils import secure_filename

class Saves():
    def __init__(self):
        self.dir = "saves/"

    def _open_json(self, folder, path):
        file_name = self.dir + folder + '/' + secure_filename(path + ".json")
        save_file = open(file_name, "r")
        return json.load(save_file)

    def get(self, folder, path, data):
        file_data = self._open_json(folder, path)
        return file_data

    def write(self, folder, path, data):
        file_data = self._open_json(folder, path)