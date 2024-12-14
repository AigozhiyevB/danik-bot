# Makefile for setting up and running the Danik Bot project

# Create a virtual environment
venv:
	python3.11 -m venv venv

# Activate the virtual environment and install dependencies
install: venv
	venv/bin/pip install -r requirements.txt

# Run the FastAPI application
run:
	venv/bin/uvicorn danik_bot.api.routes:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test:
	venv/bin/python -m unittest discover danik_bot/tests

# Clean up virtual environment and cached files
clean:
	rm -rf venv
	find . -name "__pycache__" -exec rm -rf {} +

# Build the Docker image
docker-build:
	docker build -t danik-bot .

# Run the application using Docker Compose
docker-run:
	docker-compose -f docker/docker-compose.yml up --build

