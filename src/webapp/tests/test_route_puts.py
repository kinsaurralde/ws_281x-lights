def test_index(client):
    response = client.post("/")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_data(client):
    response = client.post("/data")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"] == "JSON Decode Error"


def test_docs(client):
    response = client.post("/docs")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_colors(client):
    response = client.post("/getcolors")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_animations(client):
    response = client.post("/getanimations")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_controllers(client):
    response = client.post("/getcontrollers")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_getversioninfo(client):
    response = client.post("/getversioninfo")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_getinitialized(client):
    response = client.post("/getinitialized")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_getpixels(client):
    response = client.post("/getpixels")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_enable(client):
    response = client.post("/enable")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_disable(client):
    response = client.post("/disable")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_update(client):
    response = client.post("/update")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_getpixelsimulate(client):
    response = client.post("/getpixelsimulate")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_setpixelinterval(client):
    response = client.post("/setpixelemit")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_sequencehandler_start(client):
    response = client.post("/sequence/start")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_sequencehandler_toggle(client):
    response = client.post("/sequence/toggle")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_sequencehandler_stop(client):
    response = client.post("/sequence/stop")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_sequencestopall(client):
    response = client.post("/sequence/stopall")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_getsequences(client):
    response = client.post("/getsequences")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_404(client):
    response = client.post("/thisroutedoesnotexist")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"][:3] == "404"
