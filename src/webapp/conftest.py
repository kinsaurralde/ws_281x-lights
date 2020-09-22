import pytest

import app

# from app import app as flask_app
flask_app = app.app
socket_io = app.socketio


@pytest.fixture
def flask(mocker):
    mocker.patch("requests.post")
    yield flask_app


@pytest.fixture
def client(flask):
    return flask.test_client()


@pytest.fixture
def mocker(mocker):
    return mocker


@pytest.fixture
def background():
    return app.background


@pytest.fixture
def socketio():
    return socket_io.test_client(flask_app)


@pytest.fixture
def controller():
    # app.controllers.nosend = True
    return app.controllers
