import threading
import time
import logging
import typing
import requests
import modules

import packet_pb2 as proto_packet
import config


# pylint: disable=no-member

log = logging.getLogger(__name__)
log.setLevel("INFO")


class PacketOptions:
    def __init__(self) -> None:
        self.include_version = True
        self.include_timestamp = True


class PacketManager:
    def __init__(self, socketio, controllers, presets_config) -> None:
        self.socketio = socketio
        self.controllers = controllers
        self.packet_count = 1
        self.ping_interval = config.DEFAULT_PING_INTERVAL
        self.background_interval = config.DEFAULT_BACKGROUND_INTERVAL
        self.urls = []
        self.presets_config = presets_config
        self.version = proto_packet.Version()
        self.send_pings = False
        self.stats = modules.Stats()
        self.stats.createMetrics(["rtt", "status"])
        self.udp_sender = modules.UDPManager(self.controllers, self.stats)
        self.background_thread = None
        self.ping_thread = None

    def registerUrls(self, urls: typing.List[str]) -> None:
        for url in urls:
            self.registerUrl(url)

    def registerUrl(self, url: str) -> None:
        if url not in self.urls:
            self.urls.append(url)

    def sendList(self, items: typing.List[tuple], options=None, packet_options=None) -> None:
        for item in items:
            if len(item) < 2:
                continue
            self.send(item[0], item[1], options, packet_options)

    def send(self, url: str, payload: proto_packet.Payload, options=None, packet_options=None) -> None:
        if options is None:
            options = proto_packet.Options()
        if packet_options is None:
            packet_options = PacketOptions()
        if url not in self.urls:
            self.urls.append(url)
        packet = self._createPacket(payload, options, packet_options)
        self.udp_sender.send(url, packet)

    def setPingInterval(self, value):
        if isinstance(value, int) and value > 0:
            self.ping_interval = value

    def setBackgroundInterval(self, value):
        if isinstance(value, int) and value > 0:
            self.background_interval = value

    def setVersion(self, major=0, minor=0, patch=0, label="") -> None:
        self.version.major = major
        self.version.minor = minor
        self.version.patch = patch
        self.version.label = label

    def getVersion(self):
        options = proto_packet.Options()
        options.send_ack = True
        packet_options = PacketOptions()
        payload = proto_packet.Payload()
        payload.version.CopyFrom(proto_packet.Version())
        payload.version.major = 1
        packet = self._createPacket(payload, options, packet_options)
        print(packet, packet.SerializeToString(), len(packet.SerializeToString()))
        response = requests.post(f"http://192.168.29.100/proto", packet.SerializeToString())
        packet = proto_packet.Packet()
        print(response.content)
        packet.ParseFromString(response.content)
        # print(packet.ParseFromString(response.content))
        print(packet)

    def startBackgroundThread(self) -> None:
        self.background_thread = threading.Thread(target=self._backgroundThread, daemon=True)
        self.background_thread.start()

    def startPingThread(self) -> None:
        self.send_pings = True
        self.ping_thread = threading.Thread(target=self._pingThread, daemon=True)
        self.ping_thread.start()

    def getESPInfo(self) -> None:
        for ip in self.controllers.getControllerUrls():
            payload = proto_packet.Payload()
            payload.esp_info.is_request = True
            packet = self._createPacket(payload, proto_packet.Options(), PacketOptions())
            print(len(packet.SerializeToString()))
            response = requests.post(f"http://{ip}/proto", packet.SerializeToString())
            # packet.ParseFromString(response.content)
            print(response.content)

    @staticmethod
    def createLEDInfoPayload(led_info: dict) -> list:
        payload = proto_packet.Payload()
        if "brightness" in led_info and led_info["brightness"] is not None:
            payload.led_info.set_brightness = True
            payload.led_info.brightness = int(led_info["brightness"])
        if "frame_ms" in led_info and led_info["frame_ms"] is not None:
            payload.led_info.set_frame_ms = True
            payload.led_info.frame_ms = int(led_info["frame_ms"])
        if "frame_multiplier" in led_info and led_info["frame_multiplier"] is not None:
            payload.led_info.set_frame_multiplier = True
            payload.led_info.frame_multiplier = int(led_info["frame_multiplier"])
        print(payload)
        return payload

    def _createPacket(
        self, payload: proto_packet.Payload, options: proto_packet.Options, packet_options: PacketOptions
    ) -> proto_packet.Packet:
        packet = proto_packet.Packet()
        packet.header.CopyFrom(self._createPacketHeader(packet_options))
        packet.options.CopyFrom(options)
        packet.payload.CopyFrom(payload)
        return packet

    def _createPacketHeader(self, packet_options) -> proto_packet.Header:
        packet_header = proto_packet.Header()
        packet_header.id = self.packet_count
        if packet_options.include_version:
            packet_header.version.CopyFrom(self.version)
        if packet_options.include_timestamp:
            packet_header.timestamp_millis = int(time.time() * 1000)
        self.packet_count += 1
        return packet_header

    def _backgroundThread(self) -> None:
        while self.background_thread is not None:
            self.udp_sender.processAckQueue()
            self.socketio.emit("rtt", self.controllers.getRtt())
            time.sleep(self.background_interval)

    def _pingThread(self) -> None:
        packet_options = PacketOptions()
        options = proto_packet.Options()
        options.send_ack = True
        payload = proto_packet.Payload()
        while self.ping_thread is not None:
            if not self.send_pings:
                return
            for url in self.urls:
                ping_packet = self._createPacket(payload, options, packet_options)
                self.udp_sender.send(url, ping_packet)
            time.sleep(self.ping_interval)
