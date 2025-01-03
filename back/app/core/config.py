import os

PROJECT_NAME = "ai-agent-company-research"

TEMP_DB_URI = "postgresql+asyncpg://postgres:postgres@postgres:5432/cr"

FRONT_URL = os.getenv("FRONT_URL", "http://localhost:8080")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", TEMP_DB_URI)

GEOCODING_URL = os.getenv("GEOCODING_URL", "http://cr_geocoding:5050/api/v1/address")

SPLASH_URL = os.getenv("SPLASH_URL", "http://splash:8050/render.html")
API_KEY = os.getenv("API_KEY", ".secret/api_key.txt")
