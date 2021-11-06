import socket
import time
import threading
import logging
import packet_pb2 as proto_packet

import config

# pylint: disable=no-member

log = logging.getLogger(__name__)
log.setLevel("INFO")


class UDPManager:
    def __init__(self, controllers, stats) -> None:
        self.controllers = controllers
        self.stats = stats
        self.timeout = 1
        self.ack_thread = None
        self.background_thread = None
        self.waiting_for_ack_queue = []
        self.waiting_for_ack_queue_lock = threading.Lock()
        self.ack_queue = []
        self.ack_queue_lock = threading.Lock()
        self._startAckThread()

    def send(self, url: str, packet: proto_packet.Packet) -> None:
        thread = threading.Thread(target=self._send, args=(url, packet))
        thread.start()
        

    def processAckQueue(self) -> None:
        start_time = time.time()
        self.ack_queue_lock.acquire()
        for (ip, timestamp, raw_bytes) in self.ack_queue:
            packet = proto_packet.Packet()
            packet.ParseFromString(raw_bytes)
            rtt = timestamp - packet.header.timestamp_millis
            log.info(f"Packet {packet.header.id} from {ip} had rtt of {rtt}ms")
            self.stats.add(ip, timestamp, {"rtt": rtt, "status": packet.header.status})
            if (packet.header.id, ip) in self.waiting_for_ack_queue:
                self.waiting_for_ack_queue.remove((packet.header.id, ip))
            self.controllers.addRtt(ip, rtt)
        self.ack_queue.clear()
        self.ack_queue_lock.release()
        log.debug(f"Processing ack queue took {int((time.time() - start_time) * 1000)}ms")
        self.checkWaitingQueue()

    def checkWaitingQueue(self):
        self.waiting_for_ack_queue_lock.acquire()
        for _, ip in self.waiting_for_ack_queue:
            self.controllers.addRtt(ip, "---")
        self.waiting_for_ack_queue.clear()
        self.waiting_for_ack_queue_lock.release()

    def _send(self, url: str, packet: proto_packet.Packet):
        serialized = packet.SerializeToString()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(self.timeout)
            sock.connect((url, config.UDP_PORT))
            try:
                sock.sendall(serialized)
            except OSError:
                log.error(f"Failed to send {serialized} to {url}", exc_info=True)
            self.waiting_for_ack_queue_lock.acquire()
            self.waiting_for_ack_queue.append((packet.header.id, url))
            self.waiting_for_ack_queue_lock.release()
            log.info(f"Send packet {packet.header.id} to {url} with {len(serialized)} bytes")

    def _startAckThread(self) -> None:
        self.ack_thread = threading.Thread(target=self._ackThread, daemon=True)
        self.ack_thread.start()

    def _ackThread(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("0.0.0.0", config.ACK_PORT))
            while self.ack_thread is not None:
                data, address = sock.recvfrom(config.PACKET_BUFFER_SIZE)
                self.ack_queue_lock.acquire()
                self.ack_queue.append((address[0], int(time.time() * 1000), data))
                self.ack_queue_lock.release()
