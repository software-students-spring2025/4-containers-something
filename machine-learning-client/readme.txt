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
1. Navigate to the `machine-learning-client` directory:
   ```bash
   cd machine-learning-client
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model (if needed):
   ```bash
   python train_model.py
   ```
4. Start the ML client API:
   ```bash
   python main.py
   ```

### Run in Docker:
1. Build the Docker image:
   ```bash
   docker build -t ml-client ./machine-learning-client
   ```
2. Run the container:
   ```bash
   docker run -p 5001:5001 ml-client
   ```

## Environment Variables
- **MONGO_URI**: MongoDB connection string (e.g., `mongodb://mongodb:27017/ml_database`)
