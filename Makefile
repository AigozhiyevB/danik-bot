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

# Run tests
test:
	$(VENV_PATH)/python -m unittest discover danik_bot/tests

# Clean up virtual environment and cached files
clean:
	rm -rf venv
	find . -name "__pycache__" -exec rm -rf {} +

# Build the Docker image
docker-build:
	docker build -f docker/Dockerfile -t sandbox/danik .


run-lambda:
	docker run --platform linux/amd64 --rm --env-file .env -p 9000:8080 sandbox/danik

deploy:
	make docker-build
	docker tag sandbox/danik:latest 463224263085.dkr.ecr.eu-north-1.amazonaws.com/sandbox/danik:latest
	docker push 463224263085.dkr.ecr.eu-north-1.amazonaws.com/sandbox/danik:latest

# Run the application using Docker Compose
docker-run:
	docker-compose -f docker/docker-compose.yml up --build

