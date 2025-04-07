# Web App Subsystem (Flask)
This folder contains the Flask-based frontend of the application. It displays data collected and processed by the machine learning client, stored in MongoDB.

## How to Run

### Run locally:
```bash
cd web-app
pipenv install
pipenv run python app.py
```

### Run in Docker:
```bash
docker build -t web-app .
docker run -p 5000:5000 web-app
```

## Environment Variables
- MONGO_URI: MongoDB connection string (e.g. mongodb://mongodb:27017/your-db)