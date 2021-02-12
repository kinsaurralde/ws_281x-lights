import json
import threading
import logging
import requests

GET_TIMEOUT = 0.3
POST_TIMEOUT = 0.5

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class ControllerManager:
    """Handles sending to controllers"""

    def __init__(self, socketio, controllers, alias) -> None:
        self.session_counter = 1
        self.sessions = {}
        self.controllers = controllers
        self.alias = alias
        self.sio = socketio
        self.callbacks = {}
        self.startSession()
        print(self.controllers)

    def startSession(self) -> int:
        """Create space for threads and messages in self.sessions and return key"""
        # Assign session_id and add to self.sessions
        session_id = self.session_counter
        self.sessions[session_id] = {"threads": [], "messages": {}}
        return session_id

    def endSession(self, session_id: int) -> dict:
        """Remove session_id from self.sessions and return

        This function waits for sending threads to end and does not stop them.
        It will not return until all threads are stopped.
        """
        if session_id not in self.sessions:
            return {}
        # Wait for all threads to end
        for thread in self.sessions[session_id]["threads"]:
            thread.join()
        # Return session messages and remove from self.sessions
        result = self.sessions[session_id]["messages"]
        self.sessions.pop(session_id)
        return result

    def send(self, controller_id: int, path: str, method="GET", payload=None, threaded=True, session_id=0) -> tuple:
        """Make either GET or POST request to controller. If threaded == true start thread and return.

        If threaded is True, first value in return tuple is whether session_id is valid and second value is None
        If threaded is False, first value in return tuple indicates if an error occured. If and error occured,
        return value is the error reason else it is the response object.
        """
        # Convert aliased controller_id to url
        controller_url = self.getUrl(controller_id)
        # Check if controller exists
        if controller_url is None:
            log.error(f"Controller {controller_id} does not exist {self.controllers}")
            return False, None
        url = controller_url + path
        if threaded:
            if session_id not in self.sessions:
                return False, None
            # Create new thread and add to sessions
            thread = threading.Thread(target=self._send_thread, args=("GET", url, payload, session_id))
            thread.start()
            self.sessions[session_id]["threads"].append(thread)
            return True, None
        # Directly return response from non threading request
        return self._send_thread(method, url, payload)

    def getUrl(self, controller_id: str) -> str:
        """Return url of controller id or None if controller_id does not exist
        
        Callers of this function should check for None response
        """
        # If controller_id is an alias, convert to acutal id
        if controller_id in self.alias:
            controller_id = self.alias[controller_id]
        # Return url if controller_id exists
        if controller_id in self.controllers:
            return self.controllers[controller_id]["url"]
        return None

    def onconnectCallback(self, callback_function) -> None:
        """Set the callback function for the onconnect event"""
        self.callbacks["onconnect"] = callback_function

    def ondisconnectCallback(self, callback_function) -> None:
        """Set the callback function for the ondisconnect event"""
        self.callbacks["ondisconnect"] = callback_function

    def _send_thread(self, method: str, url: str, payload: object, session_id=0) -> tuple:
        """Make request to url with given method. If error occurs, record error_message in self.sessions"""
        error_reason = ""
        try:
            if method == "GET":
                response = requests.get(url, timeout=GET_TIMEOUT)
                self.sessions[session_id]["messages"][url] = {"success": True, "message": response}
                return True, response
            if method == "POST":
                response = requests.post(url, data=json.dumps(payload), timeout=POST_TIMEOUT)
                self.sessions[session_id]["messages"][url] = {"success": True, "message": response}
                return True, response
            error_reason = f"Invalid method: {method}"
        except requests.exceptions.Timeout:
            error_reason = "Timeout"
        except requests.RequestException as e:
            error_reason = f"Request Exception: {e}"
        except Exception as e:
            error_reason = f"Exception: {e}"
        error_message = f"Failed to send to {url} because {error_reason}"
        log.error(error_message)
        self.sessions[session_id]["messages"][url] = {"success": False, "message": error_message}
        return False, error_reason
