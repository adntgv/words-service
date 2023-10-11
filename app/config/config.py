import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")

# Redis setup
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")