
# Use the official Python image from the Docker Hub
FROM python:3.14-alpine

# Install poetry 
RUN pip install poetry==2.2.1

# Configure poetry to create the virtual environment inside the project directory
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files to the working directory
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install the dependencies
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Copy the application code to the working directory
COPY ./src /app/src

# Install the project package
RUN poetry install --without dev

# Add src to python path
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "mcwh", "--host", "0.0.0.0"]
