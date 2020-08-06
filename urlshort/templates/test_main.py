#In this we will create our first test case

from urlshort import create_app

#We create functions to test out different functionality
def test_shorten(client):               #we pass in here client so that it can act as if it was a user, using a web browser
    #We want to test and see if we can find the word Shorten on the homepage, if we found then we have set up our forms correctly
    response = client.get('/')          #first we have to visit our homepage by client.get
    assert b'Shorten' in response.data