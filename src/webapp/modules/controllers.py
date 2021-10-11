import packet_pb2 as proto_packet
import animation_pb2 as proto_animation

# pylint: disable=no-member


class Controllers:
    def __init__(self, config) -> None:
        self.controllers = {}
        self.ips = {}
        self.rtt = {}
        self.groups = {"all": []}
        self._addControllers(config.get("controllers", {}))

    def createAllControllerInitMessages(self):
        messages = []
        for controller in self.controllers:
            values = self.controllers[controller]
            led_info = proto_animation.LEDInfo()
            led_info.initialize = True
            led_info.grb = values["grb"]
            led_info.set_num_leds = True
            led_info.num_leds = values["num_leds"]
            led_info.set_brightness = values["init_brightness"]
            payload = proto_packet.Payload()
            payload.led_info.CopyFrom(led_info)
            messages.append((values["ip"], payload))
        return messages

    def createControllerInitMessage(self, ip):
        controller = self.getControllerFromIp(ip)
        if controller is None:
            return None
        values = self.controllers[controller]
        led_info = proto_animation.LEDInfo()
        led_info.initialize = True
        led_info.grb = values["grb"]
        led_info.set_num_leds = True
        led_info.num_leds = values["num_leds"]
        led_info.set_brightness = values["init_brightness"]
        payload = proto_packet.Payload()
        payload.led_info.CopyFrom(led_info)
        return payload

    def getControllerFromIp(self, ip):
        return self.ips.get(ip, None)

    def getControllerIps(self):
        return self.ips.keys()

    def addRtt(self, ip, rtt):
        self.rtt[self.getControllerFromIp(ip)] = rtt

    def getRtt(self):
        return self.rtt

    def _addControllers(self, controllers) -> None:
        for controller in controllers:
            self._addController(controller, controllers[controller])

    def _addController(self, name, config) -> None:
        if "active" not in config or not config["active"]:
            return
        if "ip" not in config:
            return
        ip = config["ip"]
        self.ips[ip] = name
        self.groups["all"].append(name)
        self.controllers[name] = {
            "ip": ip,
            "num_leds": int(config.get("num_leds", 300)),
            "init_brightness": int(config.get("init_brightness", 100)),
            "grb": bool(config.get("grb", False)),
            "enabled": bool(config.get("start_enabled", True)),
        }
