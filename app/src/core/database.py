import os
from typing import Final
import redis
from app.src.core.utils.exceptions import ObligatoryEnvIsNoneException

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# POSTGRES CONFIGURATION
POSTGRES_USER: Final[str] = os.environ.get('POSTGRES_USER', None)
POSTGRES_PASSWORD: Final[str] = os.environ.get('POSTGRES_PASSWORD', None)
POSTGRES_HOST: Final[str] = os.environ.get('POSTGRES_HOST', None)
POSTGRES_DB: Final[str] = os.environ.get('POSTGRES_DB', None)

if not POSTGRES_USER or not POSTGRES_PASSWORD or not POSTGRES_HOST or not POSTGRES_DB:
    raise ObligatoryEnvIsNoneException("One or more obligatory environment variables are not set")

SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Redis CONFIGURATION
redis_client = redis.Redis(host='redis_fastapi', port=6379, db=0, decode_responses=True)
