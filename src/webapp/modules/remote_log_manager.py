import socket
import threading
import logging

import packet_pb2 as proto_packet
import config
import modules

# pylint: disable=no-member

log = logging.getLogger(__name__)
log.setLevel("INFO")

modules.addCustomLogLevels()


class RemoteLogManager:
    def __init__(self) -> None:
        self.listen_thread = None
        self.port = config.LOG_PORT

    def start(self) -> None:
        if self.listen_thread is None:
            self.listen_thread = threading.Thread(target=self._listenThread, daemon=True)
            self.listen_thread.start()
            log.notice(f"Started Remote Log Listening Thread on Port {self.port}")
        else:
            log.warning(f"Already started Remote Log Listening Thread on Port {self.port}")

    def _listenThread(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("0.0.0.0", self.port))
            while self.listen_thread is not None:
                data, address = sock.recvfrom(512)
                log_message = proto_packet.LogMessage()
                log_message.ParseFromString(data)
                message = f"[{address[0]}]: {log_message.message}"
                if log_message.type == proto_packet.LOG_GOOD:
                    log.success(message)
                elif log_message.type == proto_packet.LOG_WARNING:
                    log.warning(message)
                elif log_message.type == proto_packet.LOG_ERROR:
                    log.error(message)
                else:
                    log.esp(message)
