#Testing allows us to make sure tha whenever we make changes to our project that we can be confident that the code we have written is unaffected and will still work for our users

#Pytest is going to be looking for this specific name whenever it is going to be running tests
import pytest
from urlshort import create_app

#Fixtures help establish the testing situation
@pytest.fixture()
def app():
    app = create_app()
    yield app 


#this fixture is to get a client so that the testing framework can act as if it was a browser and testing out the projects for us.
@pytest.fixture
def client(app):
    return app.test_client()