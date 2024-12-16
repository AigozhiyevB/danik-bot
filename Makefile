# Makefile for setting up and running the Danik Bot project
VENV_PATH = venv/bin

# Create a virtual environment
venv:
	python3.11 -m venv venv

# Activate the virtual environment and install dependencies
install: venv
	$(VENV_PATH)/pip install -r requirements.txt

# Prepare data
dataset:
	$(VENV_PATH)/python danik_bot/scripts/extract_raw.py

# Run the FastAPI application
run:
	$(VENV_PATH)/uvicorn danik_bot.api.routes:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test:
	$(VENV_PATH)/python -m unittest discover danik_bot/tests

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

