import json
import requests


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


def makeArgs():
    return {
        "debug": True,
        "test": True,
        "nosend": False,
        "config": "config/sample",
        "port": 5000,
    }


def resetControllerEnable(client):
    client.get("/disable?name=tester_b_0")
    client.get("/enable?name=tester_a_0")


def test_invalid_controller(client):
    response = client.post("/data", data=json.dumps([makeCommand()]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": 0, "message": "Controller not found", "url": "localhost"}
    ]


def test_valid_controller(client):
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert not response.get_json()["error"]
    assert response.get_json()["message"] == []


def test_disabled_controller(client):
    command = makeCommand()
    command["id"] = "tester_b_0"
    response = client.post("/data", data=json.dumps([command]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert not response.get_json()["error"]
    assert response.get_json()["message"] == []


def test_failed_to_send(client, mocker):
    mocker.patch("requests.post", side_effect=requests.RequestException)
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    print(response.get_json(), command)
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": 0, "message": "Connection Error", "url": "http://localhost:6000/data"}
    ]


def test_args_nosend_true(client, mocker, controller):
    mocker.patch("app.getNosend", return_value=True)
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": 0, "message": "No send is true", "url": "http://localhost:6000/data"}
    ]
    mocker.patch("app.getNosend", return_value=False)
    controller.setNoSend(False)


def test_enable_controller_no_arg(client):
    response = client.get("/enable")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": None, "message": "Controller not found", "url": None}
    ]


def test_enable_controller_wrong_name(client):
    response = client.get("/enable?name=doesnt_exist")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "doesnt_exist", "message": "Controller not found", "url": None}
    ]


def test_enable_controller_already_enabled(client):
    response = client.get("/enable?name=tester_a_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "tester_a_0", "message": "Controller not disabled", "url": None}
    ]


def test_enable_controller(client):
    response = client.get("/enable?name=tester_b_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert not response.get_json()["error"]
    assert response.get_json()["message"] == []
    # Test that controller enabled by trying again and checking error
    response = client.get("/enable?name=tester_b_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "tester_b_0", "message": "Controller not disabled", "url": None}
    ]
    resetControllerEnable(client)


def test_enable_controller_second_strip(client):
    response = client.get("/enable?name=tester_b_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert not response.get_json()["error"]
    assert response.get_json()["message"] == []
    response = client.get("/enable?name=tester_b_1")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "tester_b_1", "message": "Controller not disabled", "url": None}
    ]
    resetControllerEnable(client)


def test_disable_controller_no_arg(client):
    response = client.get("/disable")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": None, "message": "Controller not found", "url": None}
    ]


def test_disable_controller_wrong_name(client):
    response = client.get("/disable?name=doesnt_exist")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "doesnt_exist", "message": "Controller not found", "url": None}
    ]


def test_disable_controller_already_disabled(client):
    response = client.get("/disable?name=tester_b_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "tester_b_0", "message": "Controller not enabled", "url": None}
    ]


def test_disable_controller(client):
    response = client.get("/disable?name=tester_a_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert not response.get_json()["error"]
    assert response.get_json()["message"] == []
    # Test that controller disabled by trying again and checking error
    response = client.get("/disable?name=tester_a_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "tester_a_0", "message": "Controller not enabled", "url": None}
    ]
    resetControllerEnable(client)


def test_disable_controller_second_strip(client):
    response = client.get("/disable?name=tester_a_0")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert not response.get_json()["error"]
    assert response.get_json()["message"] == []
    response = client.get("/disable?name=tester_a_1")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": "tester_a_1", "message": "Controller not enabled", "url": None}
    ]
    resetControllerEnable(client)


def test_controller_version_info(client):
    response = client.get("/getversioninfo")
    print(response.get_json())
    assert response.status_code == 200
    assert response.content_type == "application/json"
