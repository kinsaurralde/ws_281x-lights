def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_data(client):
    response = client.get("/data")
    assert response.status_code == 405
    assert response.content_type == "text/html; charset=utf-8"


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_colors(client):
    response = client.get("/getcolors")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_animations(client):
    response = client.get("/getanimations")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_controllers(client):
    response = client.get("/getcontrollers")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_404(client):
    response = client.get("/thisroutedoesnotexist")
    assert response.status_code == 404
    assert response.content_type == "application/json"
