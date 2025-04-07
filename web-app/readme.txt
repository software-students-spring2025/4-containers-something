# Web App Subsystem (Flask)
This folder contains the Flask-based frontend of the application. It displays data collected and processed by the machine learning client, stored in MongoDB.

## How to Run

### Run locally:
1. Navigate to the `web-app` directory:
   ```bash
   cd web-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask app:
   ```bash
   python app.py
   ```

### Run in Docker:
1. Build the Docker image:
   ```bash
   docker build -t web-app ./web-app
   ```
2. Run the container:
   ```bash
   docker run -p 5002:5000 web-app
   ```

## Environment Variables
- MONGO_URI: MongoDB connection string (e.g. mongodb://mongodb:27017/your-db)