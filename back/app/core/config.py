import os

PROJECT_NAME = "ai-agent-company-research"

TEMP_DB_URI = "postgresql+asyncpg://postgres:postgres@postgres:5432/cr"

FRONT_URL = os.getenv("FRONT_URL", "http://localhost:8080")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", TEMP_DB_URI)
