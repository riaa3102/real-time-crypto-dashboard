IMAGE_NAME = crypto_dashboard
CONTAINER_NAME = crypto_dashboard_app
PORT = 8080

.PHONY: setup run build_docker run_docker stop_docker clean help

# Display help for commands
help:
	@echo "Available commands:"
	@echo "  setup         Set up the poetry environment and install dependencies"
	@echo "  run           Run the Streamlit dashboard"
	@echo "  build_docker  Build the Docker image for the project"
	@echo "  run_docker    Run the Docker container"
	@echo "  stop_docker   Stop and remove the Docker container"
	@echo "  clean         Clean the poetry environment (optional)"
	@echo "  help          Display this help message"

# Set up the poetry environment and install dependencies
setup:
	@echo "Setting up poetry environment..."
	poetry install

# Run the Streamlit dashboard
run:
	@echo "Running Streamlit dashboard..."
	poetry run streamlit run app.py --server.port $(PORT)

# Build the Docker container
build_docker:
	@echo "Building Docker image..."
	docker build . -t $(IMAGE_NAME)

# Run the Docker container
run_docker:
	@echo "Running Docker container..."
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Stop and remove the Docker container
stop_docker:
	@echo "Stopping and removing Docker container..."
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Clean the poetry environment (optional command)
clean:
	@echo "Cleaning up..."
	poetry env remove python
