# Project Athene

Project Athene is a web application for testing and interacting with LLM models. It features a FastAPI backend, PostgreSQL database, and Angular frontend (in progress).

## 🚀 Deployment Guide (Docker)

This guide assumes you are running on a machine with Docker and Docker Compose installed (e.g., Ubuntu x64).

### 1. Prerequisites

Ensure you have Docker installed on your Ubuntu machine:

```bash
# Update packages
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io docker-compose
# OR if using the newer docker compose plugin
sudo apt-get install -y docker-compose-plugin
```

Verify installation:
```bash
docker --version
docker-compose --version
```

### 2. Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd project-athene
    ```

2.  **Configure Environment Variables**:
    Create a `.env` file in the root directory. You can copy the example below:

    ```bash
    nano .env
    ```

    **Content for `.env`**:
    ```properties
    POSTGRES_USER=athene-admin
    POSTGRES_PASSWORD=your_secure_password
    POSTGRES_HOST=db  # Must be 'db' to talk to the database container
    POSTGRES_PORT=5432
    POSTGRES_DB=athene
    ```

### 3. Running the Application

Start the containers in detached mode:

```bash
sudo docker-compose up -d --build
```

Check the logs to ensure everything started correctly:

```bash
sudo docker-compose logs -f
```

### 4. Database Migrations

Once the containers are up, you **must** run the database migrations to create the tables. Run this command inside the backend container:

```bash
sudo docker-compose exec backend uv run alembic upgrade head
```

### 5. Verification

You can verify the API is active by checking the health endpoint:

```bash
curl http://localhost:8000/health
# Expected Output: {"status":"ok"}
```

## 🛠 Development Commands

# Run locally (without Docker, requires Python + uv + local Postgres)
uv run fastapi dev app/main.py