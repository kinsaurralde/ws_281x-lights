import json
import threading
import logging
import requests

from .extras import RequestResponse

GET_TIMEOUT = 0.3
POST_TIMEOUT = 0.5

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class ControllerManager:
    """Handles sending to controllers"""

    def __init__(self, controller) -> None:
        self.controller = controller
        self.session_counter = 0
        self.sessions = {}
        self.sio = self.controller.socketio
        self.latency = {}
        self.callbacks = {}
        self.nosend = False
        self.startSession()

    def startSession(self) -> int:
        """Create space for threads and messages in self.sessions and return key"""
        # Assign session_id and add to self.sessions
        session_id = self.session_counter
        self.sessions[session_id] = {"threads": [], "response": {}}
        self.session_counter += 1
        return session_id

    def addToSession(self, session_id: int, request_response=None) -> bool:
        if session_id not in self.sessions or request_response is None:
            return False
        self.sessions[session_id]["response"][request_response.controller_id] = request_response
        return True

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
        # Check if any responses were not good
        has_error = False
        error_controllers = []
        for controller_id in result:
            if not result[controller_id].good:
                has_error = True
                error_controllers.append(controller_id)
        full = {"all_good": not has_error, "responses": result, "errors": error_controllers}
        log.debug(f"End session {session_id}: {full}")
        return full

    def send(
        self, url: str, controller_id="", path="", method="GET", payload=None, session_id=0, threaded=False
    ) -> RequestResponse:
        """Make either GET or POST request to controller.

        If threaded is False, session_id is not used. For either threading option, a RequestResponse is returned.
        RequestResponse contains information about the request and the response, including if an error occured.
        In non threaded mode, the RequestResponse contains the response and possible error from the actual request.
        In threaded mode, RequestResponse error refers to whether the thread (not the request) was started correctly.
        RequestResponse from actual thread will be stored in the current session and is retrieved when session ends.
        If session_id is not the default value, it is asumed threaded is True.
        This means callers do not need to set threaded if a session_id is provided.
        """
        url += path
        if threaded or session_id != 0:
            if session_id not in self.sessions:
                return RequestResponse(None, f"Session ID {session_id} is not valid", url, controller_id)
            # Create new thread and add to sessions
            thread = threading.Thread(target=self._send_thread, args=(method, url, payload, controller_id, session_id))
            thread.start()
            self.sessions[session_id]["threads"].append(thread)
            return RequestResponse(True, f"Started Send Thread", url, controller_id)
        # Directly return response from non threading request
        return self._send_thread(method, url, payload, controller_id)

    def onconnectCallback(self, callback_function) -> None:
        """Set the callback function for the onconnect event"""
        self.callbacks["onconnect"] = callback_function

    def ondisconnectCallback(self, callback_function) -> None:
        """Set the callback function for the ondisconnect event"""
        self.callbacks["ondisconnect"] = callback_function

    def setNoSend(self, value: bool) -> None:
        self.nosend = value

    def _send_thread(self, method: str, url: str, payload: object, controller_id: str, session_id=0) -> object:
        """Make request to url with given method. If error occurs, record error_message in self.sessions"""
        error_reason = ""
        response = None
        log.debug(f"Sending {method} {url}")
        try:
            if self.nosend:
                error_reason = "No send is true"
            elif method == "GET":
                response = requests.get(url, timeout=GET_TIMEOUT)
            elif method == "POST":
                response = requests.post(url, data=json.dumps(payload), timeout=POST_TIMEOUT)
            else:
                error_reason = f"Invalid method: {method}"
            if response is not None and response.status_code != 200:
                log.warning(f"Recieved response code {response.status_code} from {url} with payload {payload}")
                log.debug(f"Error response is {response.text}")
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
