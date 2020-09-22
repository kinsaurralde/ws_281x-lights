def reset_brightness(controller):
    print(controller.getLastBrightness())
    print(controller.disabled)
    print(controller.urls)


def test_connect(socketio):
    assert socketio.get_received()[0]["name"] == "connection_response"
    assert socketio.is_connected()


def test_disconnect(socketio):
    assert socketio.is_connected()
    socketio.disconnect()
    assert not socketio.is_connected()


def test_brightness(socketio, controller):
    reset_brightness(controller)
    socketio.get_received()
    brightness = [
        {"name": "tester_a_0", "value": 100},
        {"name": "tester_a_1", "value": 101},
        {"name": "tester_c_0", "value": 102},
    ]
    socketio.emit("set_brightness", brightness)
    response = socketio.get_received()
    assert response[0]["name"] == "brightness"
    assert response[0]["args"][0] == brightness


def test_brightness_disabled(socketio, controller):
    reset_brightness(controller)
    socketio.get_received()
    brightness = [{"name": "tester_b_0", "value": 100}]
    socketio.emit("set_brightness", brightness)
    response = socketio.get_received()
    assert response[0]["name"] == "brightness"
    assert response[0]["args"][0] == brightness


def test_brightness_invalid_name(socketio):
    socketio.get_received()
    brightness = [
        {"name": "invalid_name", "value": 100},
    ]
    socketio.emit("set_brightness", brightness)
    response = socketio.get_received()
    assert response[0]["name"] == "brightness"
    assert response[0]["args"][0] == brightness


def test_loaded(socketio):
    socketio.get_received()
    socketio.emit("webpage_loaded")
    response = socketio.get_received()
    has_update = False
    has_brightness = False
    for r in response:
        if r["name"] == "update":
            has_update = True
        elif r["name"] == "brightness":
            has_brightness = True
    assert has_update
    assert has_brightness
