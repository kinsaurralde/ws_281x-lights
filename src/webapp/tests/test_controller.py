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


def test_invalid_controller(client):
    response = client.post("/data", data=json.dumps([makeCommand()]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": 0, "message": "controller not found", "url": "localhost"}
    ]


def test_valid_controller(client):
    command = makeCommand()
    command["id"] = "tester_a_0"
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
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": 0, "message": "Connection Error", "url": "http://localhost:6000/data"}
    ]


def test_args_nosend_true(client, mocker):
    args = makeArgs()
    args["nosend"] = True
    mocker.patch("app.getNosend", return_value=True)
    command = makeCommand()
    command["id"] = "tester_a_0"
    response = client.post("/data", data=json.dumps([command]))
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == [
        {"id": 0, "message": "No send is true", "url": "http://localhost:6000/data"}
    ]
