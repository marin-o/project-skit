# Project for SKIT course @FCSE


# Bookstore App

A Django-based application for managing books, authors, and publishers.

## Prerequisites

- Python 3.12+ (this is the version I used)
- PostgreSQL
- pip (Python package installer)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/marin-o/project-skit.git
    cd project-skit
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Linux use `source venv/bin/activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```dotenv
    POSTGRES_DB=bookdb
    POSTGRES_USER=bookuser
    POSTGRES_PASSWORD=bookpass
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    DJANGO_SECRET_KEY='your_secret_key'
    ```

5. **Set up the database:**

    Make sure PostgreSQL is running and create the database and user as specified in the `.env` file.

    ```sh
    psql -U postgres
    CREATE DATABASE bookdb;
    CREATE USER bookuser WITH PASSWORD 'bookpass';
    ALTER ROLE bookuser SET client_encoding TO 'utf8';
    ALTER ROLE bookuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE bookuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE bookdb TO bookuser;
    ```

6. **Apply the database migrations:**

    ```sh
    python manage.py migrate
    ```

7. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

## Running the Application

1. **Start the development server:**

    ```sh
    python manage.py runserver
    ```

2. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/`.

## Running Tests

1. **Run the tests:**

    ```sh
    pytest
    ```

2. **Run specific tests:**

    ```sh
    pytest path/to/test_file.py
    ```

## End-to-End Testing

**Run the end-to-end tests:**

    ```sh
    pytest tests/end2end/
    ```

## Directory Structure
- `Bookstore/`: Application configuration files.
- `BookstoreApp/`: Main application directory.
- `tests/`: Contains unit, integration, and end-to-end tests.
- `requirements.txt`: List of dependencies.
- `manage.py`: Django's command-line utility for administrative tasks.
