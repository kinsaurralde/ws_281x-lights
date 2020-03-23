from py.animation import Animations

class VirtualController():
    def __init__(self, name, real):
        self.real = real
        self.virtual_id = name
        self.led_count = 0
        self.a = Animations(self.led_count)
        self.controller_info = []

    def add_controller_info(self, controller_id, start, end, offset):
        template = {
            "virtual_id": self.virtual_id
        }
        template["id"] = controller_id
        template["section_id"] = str(len(self.controller_info))
        template["start"] = start
        template["end"] = end
        template["offset"] = offset
        template["length"] = end - start + 1
        self.change_led_count(end - start + 1)
        self.controller_info.append(template)

    def change_led_count(self, amount):
        self.led_count += amount
        self.a.set_led_count(self.led_count)

    def get_controller_info(self, id):
        result = {}
        for i in self.controller_info:
            if i["id"] == id:
                result[i["section_id"]] = i
        # print(result)
        return result

    def info(self):
        return {"vid": self.virtual_id, "real": self.real, "led_count": self.led_count, "controller_info": self.controller_info}

    def calc(self, actions):
        return {"layers": self.a.calc(actions), "controllers": self.controller_info}
