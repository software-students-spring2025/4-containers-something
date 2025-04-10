![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg) [![Machine Learning Client CI](https://github.com/software-students-spring2025/4-containers-something/actions/workflows/ml-client.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/4-containers-something/actions/workflows/ml-client.yml) [![Web-app CI](https://github.com/software-students-spring2025/4-containers-something/actions/workflows/web-app.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/4-containers-something/actions/workflows/web-app.yml)

# Containerized App Exercise

## Project Description

This app is an interactive app that translates ASL into the alphabet. Users can sign letters through their web camera, which will be translated into the English alphabet.

## Prerequisites

Install the following software on your machine:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installing Docker

1. Go to the [Docker website](https://www.docker.com/products/docker-desktop) and download Docker Desktop for your operating system.
2. Follow the installation instructions and make sure Docker Desktop is running.

## Running and Configuration Instructions

1. Clone the respository: 

```
git clone https://github.com/software-students-spring2025/4-containers-something.git
cd 4-containers-something
```

2. Create an .env file in the root directory with [env.example](https://github.com/software-students-spring2025/4-containers-something/blob/main/env.example):

```
MONGO_INITDB_ROOT_USERNAME=username
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_DB_NAME=database
DB_HOST=mongodb://<username>:<password>@<host>/<dbName>?authSource=<source>
URI=uriString
```

3. Create a virtual environment with `pip`

```
python -m venv .venv
source .venv/bin/activate
```

4. Run the web app (Flask) and machine learning client subsystems with the instructions under **Running Web App System** and **Running Machine Learning Subsystem**. 

5. Start all containers:

```
docker-compose up
```

### Running Web App Subsystem

#### Run Locally: 

1. Navigate to the `web-app` directory:
```
cd web-app
```

2. Install dependencies and activate environment:
```
pipenv shell
```

3. Start the Flask app:
```
python app.py
```

#### Run in Docker:

1. Build the Docker image:
```
docker build -t web-app ./web-app
```

2. Run the container:
```
docker run -p 5002:5000 web-app
```

### Running Machine Learning Subsystem

#### Run Locally: 

1. Navigate to the `machine-learning-client` directory:
```
cd machine-learning-client
```

2. Install dependencies and activate environment:
```
pipenv shell
```

3. Train the model (if needed):
```
python train_model.py
```

4. Start the ML client API:
```
python main.py
```

#### Run in Docker:

1. Build the Docker image:
```
docker build -t ml-client ./machine-learning-client
```

2. Run the container:
```
docker run -p 5001:5001 ml-client
```

## Testing
From the root directory, you can easily run the unit tests for both the client and web app code with code coverage using:

```
coverage run -m pytest machine-learning-client/ web-app/
```

## Contributors

- [Jennifer Yu](https://github.com/jenniferyuuu)
- [Iva Park](https://github.com/ivapark)
- [Chrisim Kim](https://github.com/ChrisimKim)
- [Claire Kim](https://github.com/radishsoups)

## Acknowledgements 

- Akash Nagaraj. (2018). ASL Alphabet [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/29550