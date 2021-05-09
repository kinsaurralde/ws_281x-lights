from logging import getLoggerClass, addLevelName, NOTSET

NOTICE = 25
SUCCESS = 35


class CustomLogger(getLoggerClass()):
    """Custom logging class that defines extra levels"""

    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
        addLevelName(NOTICE, "NOTICE")
        addLevelName(SUCCESS, "SUCCESS")

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
