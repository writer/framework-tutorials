# Build stage
FROM python:3.11-slim-buster AS Build

# Set environment variables for Python and Poetry
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.7.1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./pyproject.toml /app/

# Update, install dependencies, and prepare the Python environment
RUN apt-get update && \
    apt-get install -y gcc g++ unixodbc-dev && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry export --without-hashes --format requirements.txt --output requirements.txt && \
    python3 -m pip wheel --no-cache-dir --no-deps -w /app/wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim-buster AS Run

# Set environment variables for Python and Poetry
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Create a non-root user
RUN useradd -m -u 1000 user

# Switch to the non-root user
USER user

# Copy wheel files from the build stage
COPY --from=build /app/wheels $HOME/app/wheels

# Set the working directory to where the wheels are
WORKDIR $HOME/app/wheels

# Install the wheel files
RUN pip3 --no-cache-dir install *.whl

# Copy the application files to the working directory (change to your app name)
COPY --chown=user ./your-app-name $HOME/app

# Set the working directory to the application files
WORKDIR $HOME/app

# Specify the command to run the application
ENTRYPOINT [ "writer", "run" ]

# Expose the port the app runs on
EXPOSE 8080

# Set the default command to run the app
CMD [ ".",  "--port", "8080", "--host", "0.0.0.0" ]