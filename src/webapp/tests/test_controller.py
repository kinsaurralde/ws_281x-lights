import json
import requests


class MockedResponse(requests.models.Response):
    """Mocked Response"""

    def __init__(self, json_data, status_code):
        super().__init__()
        self._content = bytes(json_data)
        self.status_code = status_code


def dictToString(data):
    return json.dumps(data).encode("utf-8")


def makeCommand():
    return {
        "animation": 0,
        "color": 0,
        "color_bg": 0,
        "colors": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "arg6": False,
        "arg7": False,
        "arg8": False,
        "wait_ms": 0,
        "inc_steps": 0,
        "id": 0,
    }


def resetControllerEnable(client):
    client.get("/disable?name=tester_b_0")
    client.get("/enable?name=tester_a_0")


def check_standard_response(response, is_error, mtype=None, payload_len=0, message=None):
    response = response.get_json()
    assert "error" in response
    assert "message" in response
    assert "payload" in response
    assert "type" in response
    assert response["error"] == is_error
    assert len(response["payload"]) == payload_len
    if message is not None:
        assert response["message"] == message
    if mtype is not None:
        assert response["type"] == mtype


def test_invalid_controller(client):
    response = client.post("/data", data=json.dumps([makeCommand()]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    print(response.get_json())
    check_standard_response(response, True, "request_response", 1)


def test_valid_controller(client):
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, False, "request_response", 1)


def test_disabled_controller(client):
    command = makeCommand()
    command["id"] = "tester_b_0"
    response = client.post("/data", data=json.dumps([command]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, False, "request_response", 0)


def test_failed_to_send(client, mocker):
    mocker.patch("requests.post", side_effect=requests.RequestException)
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    print(response.get_json(), command)
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "request_response", 1)


def test_args_nosend_true(client, mocker, controller):
    mocker.patch("app.getNosend", return_value=True)
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "request_response", 1)
    mocker.patch("app.getNosend", return_value=False)
    controller.setNoSend(False)


def test_enable_controller_no_arg(client):
    response = client.get("/enable")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "enable_controller", 3, "Controller not found")


def test_enable_controller_wrong_name(client):
    response = client.get("/enable?name=doesnt_exist")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "enable_controller", 3, "Controller not found")


def test_enable_controller_already_enabled(client):
    response = client.get("/enable?name=tester_a_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "enable_controller", 3, "Controller not disabled")


def test_enable_controller(client, controller):
    start_urls = dictToString(controller.urls)
    start_disabled = dictToString(controller.disabled)
    response = client.get("/enable?name=tester_b_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, False, "enable_controller", 3, "Enabled controller")
    # Test that controller enabled by trying again and checking error
    response = client.get("/enable?name=tester_b_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "enable_controller", 3, "Controller not disabled")
    # Reset and make sure state same as before test
    resetControllerEnable(client)
    assert start_disabled == dictToString(controller.disabled)
    assert start_urls == dictToString(controller.urls)


def test_enable_controller_second_strip(client):
    response = client.get("/enable?name=tester_b_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, False, "enable_controller", 3, "Enabled controller")
    response = client.get("/enable?name=tester_b_1")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "enable_controller", 3, "Controller not disabled")
    resetControllerEnable(client)


def test_disable_controller_no_arg(client):
    response = client.get("/disable")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "disable_controller", 3, "Controller not found")


def test_disable_controller_wrong_name(client):
    response = client.get("/disable?name=doesnt_exist")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "disable_controller", 3, "Controller not found")


def test_disable_controller_already_disabled(client):
    response = client.get("/disable?name=tester_b_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "disable_controller", 3, "Controller not enabled")


def test_disable_controller(client, controller):
    start_urls = dictToString(controller.urls)
    start_disabled = dictToString(controller.disabled)
    response = client.get("/disable?name=tester_a_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    # Test that controller disabled by trying again and checking error
    response = client.get("/disable?name=tester_a_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "disable_controller", 3, "Controller not enabled")
    resetControllerEnable(client)
    assert start_disabled == dictToString(controller.disabled)
    assert start_urls == dictToString(controller.urls)


def test_disable_controller_second_strip(client):
    response = client.get("/disable?name=tester_a_0")
    print("Response", response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, False, "disable_controller", 3, "Disabled controller")
    response = client.get("/disable?name=tester_a_1")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    check_standard_response(response, True, "disable_controller", 3, "Controller not enabled")
    resetControllerEnable(client)


def test_controller_version_info(client, mocker, controller):
    controller.nosend = False
    version_info = {
        "major": 2,
        "minor": 0,
        "patch": 0,
        "esp_hash": "testing",
        "rpi_hash": "testing",
    }
    controller.version_info = version_info
    mocker.patch("requests.get", return_value=MockedResponse(dictToString(version_info), 200))
    response = client.get("/getversioninfo")
    print("Response", response.get_json())
    json_data = response.get_json()
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert json_data["fails"] == []
    assert json_data["version_match"]
    assert json_data["hash_match"]
    assert len(json_data["versioninfo"]) == 3  # Len equals num enabled controllers
    assert json_data["versioninfo"]["tester_a_0"] == version_info


def test_controller_version_info_no_hashmatch(client, mocker, controller):
    controller.nosend = False
    version_info = {
        "major": 2,
        "minor": 0,
        "patch": 0,
        "esp_hash": "testing",
        "rpi_hash": "testing",
    }
    version_info_2 = {
        "major": 2,
        "minor": 0,
        "patch": 0,
        "esp_hash": "wrong",
        "rpi_hash": "wrong",
    }
    controller.version_info = version_info_2
    mocker.patch("requests.get", return_value=MockedResponse(dictToString(version_info), 200))
    response = client.get("/getversioninfo")
    print("Response", response.get_json())
    json_data = response.get_json()
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(json_data["fails"]) > 0
    assert json_data["version_match"]
    assert not json_data["hash_match"]
    assert len(json_data["versioninfo"]) == 3  # Len equals num enabled controllers
    assert json_data["versioninfo"]["tester_a_0"] == version_info


def test_controller_version_info_no_versionmatch(client, mocker, controller):
    controller.nosend = False
    version_info = {
        "major": 2,
        "minor": 0,
        "patch": 0,
        "esp_hash": "testing",
        "rpi_hash": "testing",
    }
    version_info_2 = {
        "major": 2,
        "minor": 2,
        "patch": 2,
        "esp_hash": "testing",
        "rpi_hash": "testing",
    }
    controller.version_info = version_info_2
    mocker.patch("requests.get", return_value=MockedResponse(dictToString(version_info), 200))
    response = client.get("/getversioninfo")
    print("Response", response.get_json())
    json_data = response.get_json()
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(json_data["fails"]) > 0
    assert not json_data["version_match"]
    assert json_data["hash_match"]
    assert len(json_data["versioninfo"]) == 3  # Len equals num enabled controllers
    assert json_data["versioninfo"]["tester_a_0"] == version_info


def test_controller_initialized(client, mocker, controller):
    controller.nosend = False
    mocker.patch("requests.get", return_value=MockedResponse(dictToString([True, True]), 200))
    response = client.get("/getinitialized")
    print("Response", response.get_json())
    json_data = response.get_json()
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert json_data["fails"] == []
    for name in json_data["initialized"]:
        assert json_data["initialized"][name]


def test_controller_initialized_invalid_strip(client, mocker, controller):
    controller.nosend = False
    mocker.patch("requests.get", return_value=MockedResponse(dictToString([True]), 200))
    response = client.get("/getinitialized")
    print("Response", response.get_json())
    json_data = response.get_json()
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert json_data["fails"] == [
        {"url": "http://localhost:6000", "id": 1, "message": "Strip id does not exist on remote controller",}
    ]


def test_background_thread(background, controller):
    controller.nosend = True
    background.startLoop()
    background.active = False
