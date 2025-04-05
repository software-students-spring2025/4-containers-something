# Machine Learning Client Subsystem
This directory contains the **machine learning client** for the containerized app system.  
Its job is to collect raw data, analyze it, and store the results in a shared MongoDB database.


## What It Does
- Simulates (or eventually captures) real-world data from sensors
- Performs basic analysis or transformation on the data
- Saves both raw and processed data into a MongoDB instance
- Runs as a standalone container within a Docker Compose setup

## How to Run 

### Run Locally:
   ```bash
   cd machine-learning-client
   pipenv install
   pipenv run python main.py
   ```

### Run in Docker:
```bash
docker build -t ml-client .
docker run --env-file .env ml-Client
```

## Environment Variables
- MONGO_URI - mongodb+srv://something:<TeamSomethingContainerized>@containerized.jlgfxb3.mongodb.net/
