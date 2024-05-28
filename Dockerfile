# Use the Python 3.11 image
FROM python:3.11

# Copy the app directory into /opt/app in the Docker container
COPY ./app /opt/app
# Copy the database migrations into the Docker container
#COPY ./database /opt/database

# Copy configs into /opt/ in the Docker container
#COPY alembic.ini /opt/alembic.ini
#COPY .config.yaml /opt/app/.config.yaml

# Set working directory to /opt
WORKDIR /opt

# Install the Python dependencies
RUN python -m pip install -r app/requirements.txt

# Expose port 8080
EXPOSE 8080

# Set the command to run when the container starts
CMD python -m flask --app app/__init__.py run --host 0.0.0.0 --port 8080 --debug
