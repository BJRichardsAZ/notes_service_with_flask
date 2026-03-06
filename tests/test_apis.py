import pytest
from src.app import create_app
from src.db import init_db, get_db


# create database fixture utilizing system memory 
@pytest.fixture
def client():
    app = create_app(test_config={
        'TESTING': True,
        'DATABASE': ':memory:',
        'DEBUG': True
    })
   
    with app.app_context():
        
        init_db()                   
        
        # Create the test client INSIDE the same context/connection
        with app.test_client() as client:
            yield client


# fixture for GET tests that need data in the DB — reuses same client
@pytest.fixture
def client_with_notes(client):
    with client.application.app_context():
        db = get_db()
        db.execute("INSERT INTO notes (content) VALUES (?)", ("Need new shoes.",))
        db.execute("INSERT INTO notes (content) VALUES (?)", ("Need old shoes?.",))
        db.commit()
    return client


# create parameter variations for endpoint tests (cut down on function code)
@pytest.mark.parametrize(
    "method, endpoint, data, expected_status, expected_success, expected_message, expected_notes",
    [
         #POST when content is not provided, should result in a 400
        ("post", "/notes", None, 400, False, 'Missing required parameter: content.', None),
         #POST when content is  left empty; should result in 400 error
        ("post", "/notes", {"content": ""}, 400, False, 'Missing required parameter: content.', None),
        #POST string entered for content is longer than 250 characters, should throw an error
        ("post", "/notes", {"content": "a"*251}, 422, False, "Content parameter was over the 250 character limit.", None),
        #POST when content parameter is provided, note should post succesfully 
        ("post", "/notes", {"content": "test"}, 200, True, "Note added succesfully!", None),
    ],
)
#create test function
def test_notes_endpoint_post(client, method, endpoint, data, expected_status, expected_success, expected_message, expected_notes):
    if method == "post":
        response = client.post(endpoint, data=data or {})
    json_data = response.get_json()

    assert response.status_code == expected_status
    assert json_data["success"] == expected_success
    actual_text = str(json_data.get("error") or json_data.get("message", ""))
    assert expected_message in actual_text


# GET tests use fixture with data and without
@pytest.mark.parametrize(
    "expected_status, expected_success, expected_message, expected_notes",
    [
        #GET when db is empty; should result in success with empty array 
        (200, True, "Notes grabbed succesfully!", []),
        #GET when db is not empty, should result in 200 and display list
        (200, True, "Notes grabbed succesfully!", [
            {"content": "Need new shoes.", "id": 1},
            {"content": "Hello how are you?.", "id": 2}
        ]),
    ],
)
def test_notes_endpoint_get(client_with_notes, expected_status, expected_success, expected_message, expected_notes):
    response = client_with_notes.get("/notes")
    
    print(response)
    json_data = response.get_json()

    assert response.status_code == expected_status
    assert json_data["success"] == expected_success
    actual_text = str(json_data.get("error") or json_data.get("message", ""))
    assert expected_message in actual_text