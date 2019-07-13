import random

class Keys:
    def __init__(self, config_data):
        self.data = {
            "webkey": random.randint(1000000, 9999999)
        }
        if "keys" in config_data:
            for key in config_data["keys"]:
                self.add_key(key, config_data["keys"][key])
        print("Initial web key is", self.data["webkey"])
        self.add_key(self.data["webkey"], [-1, 0])
        self.remove_key("webkey")

    def run_function(self, function, params):
        if function == "change":
            self.change_key(params[0], params[1])
        elif function == "addstrip":
            self.add_strip(params[0], params[1])
        elif function == "removestrip":
            self.remove_strip(params[0], params[1])
        elif function == "addkey":
            if str(params[0]) not in self.data:
                self.add_key(params[0], [])
        elif function == "removekey":
            if str(params[0]) in self.data and -1 not in self.get_value(params[0]):
                self.remove_key(params[0])

    def add_key(self, key, values): 
        self.data[key] = values

    def remove_key(self, key):
        if key in self.data:
            self.data.pop(key)

    def get_value(self, key):
        return self.data[key]

    def change_key(self, old_key, new_key):
        if new_key not in self.data:
            self.add_key(new_key, self.get_value(old_key))
            self.remove_key(old_key)
            print("Key", old_key, "changed to", new_key)

    def add_strip(self, key, strip):
        if (int(strip) not in self.get_value(key)) and int(strip) != -1:
            self.get_value(key).append(int(strip))

    def remove_strip(self, key, strip):
        if (int(strip) in self.get_value(key)) and int(strip) != -1:
            self.get_value(key).remove(int(strip))

    def check_key(self, key_to_check, strip_id):
        if str(key_to_check) in self.data and key_to_check != "webkey":
            assert self.data[str(key_to_check)].count(int(strip_id)) > 0
        else:
            raise AssertionError()
        return True

    def get_keys(self, key):
        self.check_key(key, -1)
        return self.data


print("key.py loaded")
