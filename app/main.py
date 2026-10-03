from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import api_router
from app.database.database import engine, AsyncSessionLocal
from app.database.base import Base
from app.database.seed import seed_initial_diseases
from app.core.logging import setup_logging
from app.middleware.rate_limit import setup_rate_limit

from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

import logging
import os


logger = logging.getLogger(__name__)

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Creating database tables...')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info('Seeding initial data...')

    async with AsyncSessionLocal() as session:
        await seed_initial_diseases(session)

    os.makedirs('uploads/images', exist_ok=True)
    os.makedirs('knowledge_base/pdfs', exist_ok=True)
    os.makedirs('vector_store/chroma_db', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    logger.info('Database ready.')

    yield

    logger.info('Shutting down...')


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
app.add_exception_handler(
    Exception,
    global_exception_handler,
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


# Rate Limit Setup
setup_rate_limit(app)


# API Routes
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


@app.get('/')
async def root():
    return {
        'message': f'Welcome to {settings.APP_NAME}',
        'status': 'running',
        'environment': settings.ENVIRONMENT,
    }