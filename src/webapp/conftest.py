import pytest

import app

# from app import app as flask_app
flask_app = app.app


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
