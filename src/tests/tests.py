import pytest
import sqlite3
from app import create_app, get_db, init_db

#create database fixture utilizing system memory 
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'
    return client; 
#create parameter variations for endpoint tests (cut down on function code)
@pytest.mark.parametrize(
    "method, endpoint, data, expected_status, expected_success, expected_message",
    [
         #POST when content is not provided, should result in a 400
        ("post", "/notes", None, 400, False, "Missing required parameter: content.")
         #POST when content is  left empty; should result in 400 error
        ("post", "/notes", {"content": ""}, 400, False, "Missing required parameter: content."),
        #POST string entered for content is longer than 250 characters, should throw an error
        ("post", "/notes", {"content": "a"*251}, 422, False, "Content parameter was over the 250 character limit."),
        #POST when content parameter is provided, note should post succesfully 
        ("post", "/notes", {"content": "test"}, 200, True, "Note added succesfully!"),
        #GET when db is empty; should result in success with empty array 
        ("get", "/notes", None, 200, True, "Notes grabbed succesfully!"),
        #GET when db is not empty, should result in 200 and display list
        ("get", "/notes", None, 200, True, "Notes grabbed succesfully!"),
    ],
)
#create test function
def test_notes_endpoint(client, method, endpoint, data, expected_status,expected_success, expected_message):
    if method == "get":
        response = client.get(endpoint)
    elif method == "post":
        response = client.post(endpoint, data=data or {})
    json_data = response.get_json()

    assert response.status_code is expected_status
    assert json_data["success"] is expected_success
    assert expected_message in str(json_data["message"])