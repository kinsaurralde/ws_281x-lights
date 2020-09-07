import pytest

from app import app as flask_app


@pytest.fixture
def app(mocker):
    mocker.patch("requests.post")
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mocker(mocker):
    return mocker
