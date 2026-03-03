# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

A mobile-first web app that helps students quickly post, discover, and manage campus events and study groups through simple search and CRUD workflows.

## User stories

As a visitor, I want to view a list of upcoming events so that I can quickly browse what’s happening.


As a visitor, I want to open an event detail page so that I can see time, location, and full description.


As a visitor, I want to search events by keyword so that I can find relevant events faster.


As a visitor, I want to filter/search events by tag or location so that I can narrow results to my interests.


As a student organizer, I want to create a new event so that I can invite others to join.


As a student organizer, I want to edit an event I posted so that I can update changes like time or location.


As a student organizer, I want to delete an event I posted so that outdated or canceled events are removed.


As a student organizer, I want to see a confirmation before deleting so that I don’t remove events by accident.


As a user, I want to see clear form validation errors so that I know how to fix missing or invalid inputs.


As a user, I want the app to be easy to use on a phone screen so that I can operate it comfortably on mobile.


## Steps necessary to run the software

1. Clone the repository and enter the project folder:
   git clone <REPO_URL>
   cd 2-web-app-velvet_vipers

2. Install dependencies using Pipenv:
   pip install pipenv
   pipenv install

3. Configure environment variables:
   - Copy env.example to .env and fill in values as needed:
     cp env.example .env
   - Make sure your MongoDB connection info in .env is correct (example):
     MONGO_URI=mongodb://localhost:27017
     MONGO_DB_NAME=appdb

4. Start MongoDB (choose ONE):
   - Option A (Docker):
     docker run --name mongo-local -p 27017:27017 -d mongo:7
   - Option B (Local install):
     Ensure MongoDB is running and accessible at mongodb://localhost:27017

5. Run the application:
   pipenv run python3 run.py

6. Open the app in your browser:
   http://127.0.0.1:5000

   
## Task boards

Link for Sprint 1: https://github.com/orgs/swe-students-spring2026/projects/36
Link for Sprint 2: https://github.com/orgs/swe-students-spring2026/projects/69
