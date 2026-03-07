# Notes Vault API

A simple back-end service for posting and retrieving notes in a persistant database; all containerized in Docker. 

## Overview

This project implements a small backend service that allows users to create, view, and delete notes. It was developed as a coding challenge to demonstrate clean REST API design, data persistence, automated testing, and easy distribution via Docker.

## Tech Stack & Rationale

- **Framework**: Flask – lightweight and excellent for quickly building REST APIs in Python.
- **Database**: SQLite (using Python’s built-in `sqlite3` module) – serverless, file-based, zero-configuration persistence.
- **Testing**: pytest – clean, powerful, and ideal for both unit and integration tests.
- **Containerization**: Docker + Docker Compose – allows anyone to run the full service with a single command, no local Python or database setup required.


I chose this stack to showcase not just python but my ability to learn new frameworks while keeping the solution simple, maintainable, and easy to evaluate.

## System Overview

The service provides a REST API for managing notes. Each note contains:
- `id` – auto-incrementing integer primary key
- `content` – text (maximum 250 characters)
- `createdAt` – timestamp automatically set on creation

Features include:
- Per-request lazy database connections (fresh connection per HTTP request)
- Input validation and custom error handling with consistent JSON responses
- Multi-stage Docker build that runs all tests before producing the final image
- Persistent data stored in a Docker volume (survives container restarts)

## API Endpoints

| Method | Endpoint           | Description                  |
|--------|--------------------|------------------------------|
| GET    | `/notes`           | List all notes               |
| POST   | `/notes`           | Create a new note            |
| GET    | `/notes/{id}`      | Get a note by ID             |
| DELETE | `/notes/{id}`      | Delete a note by ID          |

### Usage Examples

**Get all notes**
curl http://localhost:5000/notes

**Create a new note**
curl -X POST http://localhost:5000/notes -d "content=Buy groceries"

**Get a note by ID**
curl http://localhost:5000/notes/{id}

**Delete a note by ID**
curl -X DELETE http://localhost:5000/notes/{id}

All succesful responses follow this structure: 
{
  "success": true,
  "message": "Notes grabbed succesfully!",
}

Error responses return appropriate HTTP status codes (400, 404, 422, 500) with:
{
  "success": false,
  "error": "error message"
}

# Quick Start (Docker)

## Requirements: 
Docker and Docker Compose installed and running

### 1. Clone the repository
git clone https://github.com/BJRichardsAZ/notes_service_with_flask.git

### 2. In the project directory, start the service
docker compose up --build -d app

### 3. Test it
curl http://localhost:5000/notes

### Data Persistance
The SQLITE database is stored in a named Docker volume and data should persists across container restarts, rebuilds, and docker compose down

## Persistance Demo 
curl -X POST http://localhost:5000/notes -d "content=This note survives restarts!"
docker compose down
docker compose up -d app
curl http://localhost:5000/notes   # ← note is still present

if you need to clear the database for some reason, you should be able to invoke our cli command for calling init_db which will drop the existing table:

docker compose exec app flask --app src.app init_db

### Improvements and Tradeoffs

## Tradeoffs:

- SQLite was chosen for simplicity (great for small scale, but write-lock behavior limits high concurrency)
- Used Flask’s built-in development server (fine for a demo, not production-ready)
- No authentication (kept scope minimal per the challenge requirements)

## Future Improvements:

- Migrate to PostgreSQL + SQLAlchemy for better scalability and concurrency
- Add authentication (API keys or JWT)
- Implement update endpoint, search by content/date, and note titles
- Return the new note ID in POST responses
- Replace dev server with Gunicorn for production use

### Project Structure

notes_service_with_flask/
├── src/
│   ├── app.py
│   ├── db.py
│   ├── errors.py
│   └── blueprints/notes.py
├── tests/
│   ├── test_apis.py
│   └── test_business_logic.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── schema.sql
└── README.md

### (extra) personal notes while creating the system: 
-	Begin by learning how to implement an instance of an app in flask; for concurrent requests, it’s much more efficient to create a helper function that establishes a new “lazy” connection to the db. This function will additionally detect data types of columns and translate database rows from tuple into sqlite3.row objects.
-	We also create a route function that initializes the db; the schema for the notes table is contained in a separate file and called when the db is initialized; if the table does not exist in the db file, it will be created.
-	Also create a cli command to initialize the db, so that we can reset table(s) if needed. 
-	Create endpoint routes for http requests; include simple try exception blocks to return success or failure messages based on standardized error codes. 
-	At this stage, note that in the console I am seeing that the default timestamp converter has been deprecated in this version of python, either change this conversion method or highlight in later read me section
-	Create centralized error handling and refactor api routes; remove/avoid throwing try exception blocks directly in routes as in production this is not ideal 
-	Build endpoint for specific note retrieval/deletion; I had to take note of differing syntax here between flask/python and other languages I’ve used prior. 
-	Now create some simple unit tests for detecting expected outputs of api requests, parameterize them using pytest parameterize constructor so we can write one function and provide different parameters to it (even different endpoints, this will make it easily scalable when adding endpoints)
-	When running the tests, it seems the naming convention of the file is integral to pytest (needs to start with the word test), but also the import structure is very important. 
-	At this stage, need to restructure the files so that we can clearly define pieces as modules/packages for easier imports when running integration/unit tests; this foregoes needing to interact/manipulate the sys.path when running things. Also run pytest as module (python -m pytest etc)
-	After running initial tests, an issue in the architecture was exposed; initially when beginning I implemented route creation for the flask app directly in the same file outside of our create_app function(this only really works in single file application formats), meaning when creating our app in the test file we do not have access to our routes; two solutions present themselves, create the routes as blueprints and register  them  in create_app or directly put route creation code in our function. I will move to create them as blueprints and register them since this is a more standard approach. 
-	Tests kept failing due to an issue with fresh database instances being created without the proper table being present – due to a duplicitous context being passed in init_db. It’s since been removed and the issue resolved for four of the six initial tests. 
-	Resolved the remaining two tests failing because of a table creation error; this was done by allowing the connection  created in the fixture to share the same location in the cache when creating an app instance in system memory
-	Created simple business logic tests in a separate unit test file to test connection lifecycle and respect for table schema (left out close connection tests for brevity, but would be easy enough to add when extending these.)
-	Unit test creation took more time then expected but it was due to needing to learn some of the intricacies/behavior of flask, and how to properly keep connections made in fixture alive between requests to ensure tables existed in db
-	Now that main project files are complete, lets containerize it for ease of use for reviewers
-	Create requirements.txt with dependencies and a dockerfile as well as the .yaml; put everything into github 
