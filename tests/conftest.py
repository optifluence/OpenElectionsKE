import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models import Base
from app.main import application as app
from app.database import get_db
import app.database
import asyncio

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Patch the app's engine and sessionmaker to use the test ones
app.database.engine = engine
app.database.AsyncSessionLocal = TestingSessionLocal

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(prepare_database):
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="function")
def test_app(db_session, monkeypatch, prepare_database):
    # Patch get_db to use the test sessionmaker
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
