import pytest
import app

@pytest.fixture
def client():
    app_test = app.app

    app_test.config["TESTING"] = True
    app_test.testing = True

    client = app_test.test_client()
    yield client

def test_app(client):
    rv = client.get('/')
    assert b'hello :)' in rv.data

#def test_app_version(client):
#    rv = client.get('/return_version')
#    assert b'version 3.0' in rv.data
