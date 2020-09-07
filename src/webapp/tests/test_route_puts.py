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


def test_404(client):
    response = client.post("/thisroutedoesnotexist")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.get_json()["error"]
    assert response.get_json()["message"][:3] == "404"
