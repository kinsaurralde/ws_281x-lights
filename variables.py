class Variables:
    def __init__(self):
        self.data = {}

    def _create(self, name, value, v_type = None):
        var = {
            "name": None,
            "type": None,
            "value": value
        }
        var["name"] = name
        if v_type == "color":
            var["type"] = "color"
        if type(value) == type(int()):
            var["type"] = "int"
        if v_type == "function":
            var["type"] = "function"
        var["value"] = value
        return var

    def exists(self, name):
        if name in self.data:
            return True
        return False

    def add(self, name, value, v_type = None):
        self.data[name] = self._create(name, value, v_type)

    def get(self, name):
        if self.exists(name):
            return self.data[name].value

    def get_type(self, name):
        if self.exists(name):
            return self.data[name].type
        return None

    def list_all(self):
        for v in self.data:
            c = self.data[v]
            print(c["name"], c["type"], c["value"])
        return self.data

    def info(self):
        return self.data

    def p_values(self, data):
        if not isinstance(data, dict):
            return data
        c = data.copy()
        for k in data:
            if isinstance(data[k], dict):
                c[k] = self.p_values(data[k])
            elif isinstance(data[k], list):
                c[k] = []
                for i in data[k]:
                    c[k].append(self.p_values(i))
            elif str(data[k])[0] == '$':
                name = str(data[k])[1:]
                if name in self.data:
                    c_type = self.data[name]["type"]
                    if c_type == "int":
                        c[k] = int(self.data[name]["value"])
                    elif c_type == "color":
                        c["r"] = int(self.data[name]["value"][0])
                        c["g"] = int(self.data[name]["value"][1])
                        c["b"] = int(self.data[name]["value"][2])
                        c.pop("color")
                    elif c_type == "function":
                        c[k] = self.data[name]["value"]
        return c