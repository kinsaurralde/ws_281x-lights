import random

class Keys:
    def __init__(self, config_data):
        self.data = {
            "webkey": random.randint(1000000, 9999999)
        }
        if "keys" in config_data:
            for key in config_data["keys"]:
                # self.data[key] = config_data["keys"][key]
                self.add_key(key, config_data["keys"][key])
        print("Initial web key is", self.data["webkey"])
        self.add_key(self.data["webkey"], [-1, 0])
        self.remove_key("webkey")

    def add_key(self, key, values):
        self.data[key] = values

    def remove_key(self, key):
        if key in self.data:
            self.data.pop(key)

    def get_value(self, key):
        return self.data[key]

    def change_key(self, old_key, new_key=None):
        if new_key == None:
            # self.data[old_key] = str(random.randint(1000000, 9999999))
            self.add_key(str(random.randint(1000000, 9999999)), self.get_value(old_key))
        else:
            # self.data[old_key] = new_key
            self.add_key(new_key, self.get_value(old_key))
        self.remove_key(old_key)
        
        print("Key", old_key, "changed to", new_key)

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
