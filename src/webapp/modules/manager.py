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
        self.sessions[session_id] = {"threads": [], "response": {}}
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
        result = self.sessions[session_id]["response"]
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
            error_message = f"Controller {controller_id} does not exist"
            log.error(error_message)
            return RequestResponse(None, error_message, controller_id=controller_id)
        url = controller_url + path
        if threaded:
            if session_id not in self.sessions:
                return RequestResponse(None, f"Session ID {session_id} is not valid", url, controller_id)
            # Create new thread and add to sessions
            thread = threading.Thread(target=self._send_thread, args=("GET", url, payload, controller_id, session_id))
            thread.start()
            self.sessions[session_id]["threads"].append(thread)
            return RequestResponse(True, f"Started Send Thread", url, controller_id)
        # Directly return response from non threading request
        return self._send_thread(method, url, payload, controller_id)

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

    def _send_thread(self, method: str, url: str, payload: object, controller_id: str, session_id=0) -> object:
        """Make request to url with given method. If error occurs, record error_message in self.sessions"""
        error_reason = ""
        response = None
        try:
            if method == "GET":
                response = requests.get(url, timeout=GET_TIMEOUT)
            elif method == "POST":
                response = requests.post(url, data=json.dumps(payload), timeout=POST_TIMEOUT)
            else:
                error_reason = f"Invalid method: {method}"
        except requests.exceptions.Timeout as e:
            error_reason = "Timeout: {e}"
        except requests.RequestException as e:
            error_reason = f"Request Exception: {e}"
        except Exception as e:
            error_reason = f"Exception: {e}"
        result = RequestResponse(response, error_reason, url)
        self.sessions[session_id]["response"][controller_id] = result
        if result.good:
            return result
        error_message = f"Failed to send to {url} because {error_reason}"
        log.error(error_message)
        return result


class RequestResponse:
    def __init__(self, response, message="", url="", controller_id="") -> None:
        self.good = False if response is None else True
        self.has_response = True if self.good and not isinstance(response, bool) else False
        self.response = response
        self.message = message
        self.url = url
        self.controller_id = controller_id
