import json
import threading
import requests

GET_TIMEOUT = 0.3
POST_TIMEOUT = 0.5

class ControllerManager:
    def __init__(self, socketio, controllers, alias) -> None:
        self.session_counter = 1
        self.sessions = {}
        self.controllers = controllers
        self.alias = alias
        self.sio = socketio
        self.callbacks = {}

    def startSession(self):
        session_id = self.session_counter
        self.sessions[session_id] = {
            'threads': [],
            'messages': {}
        }
        return session_id

    def endSession(self, session_id):
        if session_id not in self.sessions:
            return {}
        for thread in self.sessions[session_id]['threads']:
            thread.join()
        result = self.sessions[session_id]['messages']
        self.sessions.pop(session_id)
        return result

    def send(self, controller_id, path, method="GET", payload=None, threaded=True, session_id=0):
        url = self.getUrl(controller_id) + path
        if threaded:
            if session_id not in self.sessions:
                return False, None
            thread = threading.Thread(
                target=self._sending_thread, args=(url, payload, controller_id, session_id)
            )
            thread.start()
            self.sessions[session_id]['threads'].append(thread)
            return True, None
        return self._send_thread(method, url, payload)

    def getUrl(self, controller_id) -> str:
        if controller_id in self.alias:
            return self.alias[controller_id]
        return controller_id

    def onconnectCallback(self, callback_function) -> None:
        self.callbacks['onconnect'] = callback_function

    def ondisconnectCallback(self, callback_function) -> None:
        self.callbacks['ondisconnect'] = callback_function

    def _send_thread(self, method, url, payload, session_id) -> tuple:
        error_reason = ""
        try:
            if method == "GET":
                response = requests.get(url, timeout=GET_TIMEOUT)
                self.sessions[session_id]['messages'].append({'success': True, 'message': response})
                return True, response
            elif method == "POST":
                response = requests.post(url, data=json.dumps(payload), timeout=POST_TIMEOUT)
                self.sessions[session_id]['messages'].append({'success': True, 'message': response})
                return True, response
            error_reason = f"Invalid method: {method}"
        except requests.exceptions.Timeout:
            error_reason = "Timeout"
        except requests.RequestException as e:
            error_reason = f"Request Exception: {e}"
        except Exception as e:
            error_reason = f"Exception: {e}"
        error_message = f"Failed to send to {url} because {error_reason}"
        print(error_message)
        self.sessions[session_id]['messages'].append({'success': False, 'message': error_message})
        return False, error_reason
