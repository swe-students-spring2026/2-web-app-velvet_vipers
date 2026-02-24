# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

See instructions. Delete this line and place the Product Vision Statement here.

## User stories

See instructions. Delete this line and place a link to the user stories here.

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

See instructions. Delete this line and place a link to the task boards here.
