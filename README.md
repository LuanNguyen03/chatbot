# Banking AI Project Deployment Guide

This guide will help you set up and deploy the Banking AI project after cloning from GitHub.

## 1. Clone the Repository

```
git clone <your-repo-url>
cd banking_AI
```

## 2. Set Up Python Environment

- Recommended: Python 3.9+
- Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

## 3. Install Dependencies

```
pip install -r requirements.txt
```

## 4. Database Setup

- Configure your database connection in `app/config.py` if needed.
- Initialize the database (using Alembic for migrations):

```
alembic upgrade head
```

## 5. Run the Application

```
uvicorn app.main:app --reload
```

- The app will be available at: http://127.0.0.1:8000

## 6. Access the Web UI

- Open your browser and go to: http://127.0.0.1:8000
- Login or register to use the system.

## 7. API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## 8. Running Tests

- (If tests are available)

```
pytest
```

## 9. Notes

- Make sure your database server is running and accessible.
- For production, configure environment variables and use a production-ready server (e.g., Gunicorn, Uvicorn with workers).
- Update `alembic.ini` and `app/config.py` for your environment as needed.

## 10. Advanced Deployment & Customization

### a. Environment Variables & Configuration

- Use environment variables for sensitive data (DB connection, secret keys, etc.).
- Example (Windows):
  ```cmd
  set DATABASE_URL=postgresql://user:password@localhost:5432/banking_ai
  set SECRET_KEY=your_secret_key
  ```
- Or create a `.env` file and use `python-dotenv`.

### b. Production Deployment

- Use a production server:
  - Gunicorn (Linux):
    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
    ```
  - Uvicorn with multiple workers (Windows):
    ```cmd
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    ```
- Set `debug=False` and configure logging as needed.

### c. Database Migration & Backup

- Use Alembic for schema migrations:
  ```
  alembic revision --autogenerate -m "Describe change"
  alembic upgrade head
  ```
- Regularly backup your database (PostgreSQL, MySQL, etc.).

### d. Security Best Practices

- Change default admin credentials after first login.
- Use HTTPS in production (with a reverse proxy like Nginx or Caddy).
- Set strong `SECRET_KEY` and secure session/cookie settings.
- Regularly update dependencies to patch vulnerabilities.

### e. Customization

- Add new business logic by creating new routers in `app/routers/` and templates in `app/templates/`.
- Update models in `app/models.py` and run Alembic migrations for DB changes.
- Use AJAX in templates for dynamic UI (see existing templates for examples).

### f. Troubleshooting

- Check logs in the terminal for errors.
- Use `alembic current` and `alembic history` to debug DB migration issues.
- For CORS/API issues, check FastAPI CORS middleware settings in `main.py`.

---

# Detailed Instructions for Each Step

## 1. Clone the Repository

- Replace `<your-repo-url>` with your actual repository URL from GitHub.
- Example:
  ```bash
  git clone https://github.com/yourusername/banking_AI.git
  cd banking_AI
  ```

## 2. Set Up Python Environment

- Make sure Python 3.9 or higher is installed. Download from https://www.python.org/downloads/
- To create a virtual environment:
  ```bash
  python -m venv venv
  ```
- To activate on Windows:
  ```cmd
  venv\Scripts\activate
  ```
- To activate on Linux/Mac:
  ```bash
  source venv/bin/activate
  ```
- You should see `(venv)` in your terminal prompt.

## 3. Install Dependencies

- Make sure your virtual environment is activated.
- Install all required packages:
  ```bash
  pip install -r requirements.txt
  ```
- If you see errors, ensure you are using the correct Python version and that `pip` is available.

## 4. Database Setup

- By default, the project uses the database settings in `app/config.py`. Edit this file to match your local or production database.
- Example for PostgreSQL:
  ```python
  SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/banking_ai"
  ```
- To initialize the database schema, run:
  ```bash
  alembic upgrade head
  ```
- If you need to create a new migration after changing models:
  ```bash
  alembic revision --autogenerate -m "Describe your change"
  alembic upgrade head
  ```

## 5. Run the Application

- Start the FastAPI server in development mode:
  ```bash
  uvicorn app.main:app --reload
  ```
- The `--reload` flag auto-restarts the server on code changes (for development only).
- Open http://127.0.0.1:8000 in your browser to check if the app is running.

## 6. Access the Web UI

- Go to http://127.0.0.1:8000 in your browser.
- Register a new user or log in with existing credentials.
- Explore the navigation bar for all features (accounts, transactions, products, etc.).

## 7. API Documentation

- FastAPI auto-generates API docs:
  - Swagger UI: http://127.0.0.1:8000/docs
  - Redoc: http://127.0.0.1:8000/redoc
- You can test API endpoints directly from these pages.

## 8. Running Tests

- If the `tests/` folder contains test files, run:
  ```bash
  pytest
  ```
- Make sure the app and database are configured for testing (use a test DB if possible).

## 9. Notes

- If you change database settings, restart the app.
- For production, do not use `--reload` and set up a proper server (see below).
- Always keep your dependencies up to date:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

## 10. Advanced Deployment & Customization

### a. Environment Variables & Configuration

- Store sensitive info (DB URL, secret keys) in environment variables or a `.env` file.
- Example `.env` file:
  ```env
  DATABASE_URL=postgresql://user:password@localhost:5432/banking_ai
  SECRET_KEY=your_secret_key
  ```
- Use the `python-dotenv` package to load `.env` automatically.
- In `app/config.py`, load variables using `os.environ.get()`.

### b. Production Deployment

- Use a process manager and production server:
  - Gunicorn (Linux):
    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
    ```
  - Uvicorn with workers (Windows):
    ```cmd
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    ```
- Use Nginx or Caddy as a reverse proxy for HTTPS and static files.
- Set `debug=False` in your config and configure logging.

### c. Database Migration & Backup

- Use Alembic for all schema changes:
  ```bash
  alembic revision --autogenerate -m "Describe change"
  alembic upgrade head
  ```
- Backup your database regularly using your DBMS tools (e.g., `pg_dump` for PostgreSQL).

### d. Security Best Practices

- Change all default passwords after setup.
- Use HTTPS in production (see Nginx/Caddy docs).
- Set a strong `SECRET_KEY` in your environment.
- Regularly update dependencies:
  ```bash
  pip install --upgrade -r requirements.txt
  ```
- Review FastAPI security docs: https://fastapi.tiangolo.com/advanced/security/

### e. Customization

- To add a new business feature:
  1. Create a new model in `app/models.py`.
  2. Add a schema in `app/schemas.py`.
  3. Create a router in `app/routers/` and register it in `main.py`.
  4. Add a template in `app/templates/` for the UI.
  5. Run Alembic migrations if the DB schema changes.
- For AJAX UI, see examples in existing templates (e.g., `accounts.html`).

### f. Troubleshooting

- If the app won't start, check the terminal for errors.
- For DB errors, check your connection string and DB server status.
- For migration issues:
  ```bash
  alembic current
  alembic history
  ```
- For CORS/API issues, check FastAPI CORS middleware in `main.py`.
- For more help, see FastAPI docs: https://fastapi.tiangolo.com/

---

**For any issues, please open an issue on the repository or contact the maintainer.**
