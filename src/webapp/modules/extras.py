import json
import logging

import yaml


NOTICE = 25
SUCCESS = 35


class CustomLogger(logging.getLoggerClass()):
    """Custom logging class that defines extra levels"""

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        logging.addLevelName(NOTICE, "NOTICE")
        logging.addLevelName(SUCCESS, "SUCCESS")

    def notice(self, msg, *args, **kwargs):
        if self.isEnabledFor(NOTICE):
            self._log(NOTICE, msg, args, **kwargs)

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)


class RequestResponse:
    """Contains response fields and error status"""

    def __init__(self, response, message="", url="", controller_id="") -> None:
        self.good = False if response is None else True  # pylint: disable=simplifiable-if-expression
        self.has_response = False
        if self.good and not isinstance(response, bool):  # pylint: disable=simplifiable-if-expression
            self.has_response = True
        self.response = response
        self.message = message
        self.url = url
        self.controller_id = controller_id


def createResponse(app, payload):
    """Turn response into json"""
    try:
        payload = json.dumps(payload, sort_keys=False)
    except TypeError:
        payload = json.dumps(
            {
                "good": False,
                "type": "serialization_error",
                "message": "Failed to serialize response into JSON",
                "payload": {},
            }
        )
    response = app.response_class(response=payload, status=200, mimetype="application/json",)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def errorResponse(app, message):
    """Create error response"""
    data = {
        "error": True,
        "message": message,
    }
    return createResponse(app, data)


def responseTemplate(good=False, mtype="", message="", payload=None):
    if payload is None:
        payload = {}
    return {"good": good, "type": mtype, "message": message, "payload": payload, "error": not good}


def openYaml(path):
    """Open yaml file and return as a dictionary"""
    data = {}
    with open(path) as open_file:
        data = yaml.safe_load(open_file)
    return data
