```markdown
# Mitul Bhai Backend API

A robust, production-ready backend application built with FastAPI and PostgreSQL. This API features a complete authentication system utilizing JSON Web Tokens (JWT) with both short-lived access tokens and long-lived refresh tokens, all fully containerized with Docker.

## 🚀 Features

* **FastAPI Framework:** High-performance async routing and automatic OpenAPI documentation.
* **PostgreSQL Database:** Relational data storage managed via SQLAlchemy ORM.
* **JWT Authentication:** Secure login system with access (30 min) and refresh (7 day) tokens.
* **Password Hashing:** Industry-standard `bcrypt` encryption via `passlib`.
* **Containerized Deployment:** Seamless orchestration using Docker and Docker Compose (V2).
* **Dependency Injection:** Reusable dependencies for database sessions and route protection.

---

## 📋 Prerequisites

Before running the application, ensure you have the following installed on your machine:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose (V2)](https://docs.docker.com/compose/install/)

---

## 🛠️ Quickstart

The easiest way to run the project is using Docker Compose. It will automatically build the web environment, initialize the PostgreSQL database, and handle networking between the two.

**1. Clone the repository and navigate to the root directory.**

**2. Build and start the containers in detached mode:**
```bash
docker compose up --build -d

```

**3. Access the API Documentation:**
Once the containers are running and the database healthcheck passes, open your browser and navigate to the built-in Swagger UI:

* **http://localhost:8000/docs**

**4. Stop the containers:**

```bash
docker compose down

```

---

## 🌐 API Endpoints

| Method | Endpoint | Description | Auth Required |
| --- | --- | --- | --- |
| `POST` | `/register` | Creates a new user in the PostgreSQL database. | No |
| `POST` | `/login` | Authenticates a user and returns access and refresh tokens. | No |
| `POST` | `/refresh` | Accepts a valid refresh token and issues a new token pair. | No |
| `GET` | `/users/me` | Returns the profile data of the currently authenticated user. | Yes (Access Token) |

---

## 💻 Local Development (Without Docker)

If you prefer to run the FastAPI application locally using your Conda environment for faster iteration:

**1. Ensure a local PostgreSQL instance is running on port 5432.**

**2. Update your `database.py` connection string to point to `localhost`:**

```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/myappdb"

```

**3. Install dependencies:**

```bash
pip install -r requirements.txt

```

**4. Run the Uvicorn development server:**

```bash
uvicorn main:app --reload

```

```



```