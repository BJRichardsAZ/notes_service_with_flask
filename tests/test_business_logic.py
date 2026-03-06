import pytest
from src.db import get_db, close_db, init_db
from src.app import create_app
from flask import g




@pytest.fixture
def app():
  # we must create an active flask instance similar to our api tests

    return create_app(test_config={
        'TESTING': True,
        'DATABASE': ':memory:'
    })
        
# ---  Test connection Behaviors ---
#confirm we are re-using the existing connection(same python object is returned when openin)
def test_get_db_reuses_same_connection_inside_same_request(app):

 with app.app_context():
    assert 'db' not in g
    db1 = get_db()
    db2 = get_db()

    #confirm lazy connection
    assert 'db' in g
    #confirm same connection
    assert db1 is db2
    #confirm same object
    assert id(db1) == id(db2)

#confirm fresh connections are made between different requests
def test_get_db_uses_fresh_singleton_connection_between_requests(app):
    with app.app_context():
        dbrq1 = get_db()
    with app.app_context():
        dbrq2 = get_db()

    assert dbrq1 is not dbrq2
    assert id(dbrq1) != id(dbrq2)


#-- Test init db behaviors --
def test_init_db_creates_tables_and_respects_schema(app):
    with app.app_context():
        init_db()

        #assert that a table named notes is fetched and created
        db = get_db()
        cursor = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='notes'"
        )
        assert cursor.fetchone() is not None

        #verify column designations and defautl values
        cursor = db.execute("PRAGMA table_info(notes)")
        columns = {row['name'] for row in cursor.fetchall()}
        assert columns == {'id', 'content', 'createdAt'}


def test_init_db_drops_existing_table_before_recreating(app):
    with app.app_context():
        # manually create a table
        db = get_db()
        db.execute("CREATE TABLE notes (old_id INTEGER)")
        db.commit()

        init_db()   
        #this should drop the manually created table 
        cursor = db.execute("PRAGMA table_info(notes)")
        columns = {row['name'] for row in cursor.fetchall()}
        assert 'content' in columns
        assert 'createdAt' in columns
        assert 'old_id' not in columns






    