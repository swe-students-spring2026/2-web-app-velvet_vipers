# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

---

# Product vision statement

A mobile-first web app that helps students quickly post, discover, and manage campus events and study groups through simple search and CRUD workflows.

---

# User stories

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

---

# Prerequisites

Before running the application, make sure the following tools are installed:

* **Python 3**
* **pipenv**
* **MongoDB** (local installation or Docker)

---

# Steps necessary to run the software

## 1. Clone the repository

```bash
git clone <REPO_URL>
cd 2-web-app-velvet_vipers
```

---

## 2. Install dependencies

```bash
pip install pipenv
pipenv install
```

---

## 3. Configure environment variables

Copy the example environment file:

```bash
cp env.example .env
```

Edit `.env` and set your MongoDB connection info:

```env
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=campus_events_db
SECRET_KEY=your-secret-key
```

**Notes**

* `MONGODB_URI` specifies the MongoDB connection address
* `DB_NAME` is the name of the database used by the application
* `SECRET_KEY` is used by Flask for session security

Do **not commit the `.env` file** to version control.

---

## 4. Start MongoDB (choose ONE)

### Option A — Docker (recommended)

```bash
docker run --name mongo-local -p 27017:27017 -d mongo:7
```

### Option B — Local installation

Ensure MongoDB is running locally and accessible at:

```
mongodb://localhost:27017
```

---

## 5. Run the application

```bash
pipenv run python3 run.py
```

---

## 6. Open the app in your browser

```
http://127.0.0.1:5001
```

---

# Troubleshooting

**MongoDB connection error**

Make sure MongoDB is running and that the connection string in `.env` is correct.

**Port already in use**

If port `5001` is already in use, stop the conflicting process or change the port in the application configuration.

**Dependency errors**

Run the following again:

```bash
pipenv install
```

---

# Task boards

Link for Sprint 1:
https://github.com/orgs/swe-students-spring2026/projects/36

Link for Sprint 2:
https://github.com/orgs/swe-students-spring2026/projects/69
