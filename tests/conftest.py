import os
from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture(scope="session")
def test_database(tmp_path_factory: pytest.TempPathFactory) -> str:
    db_path = tmp_path_factory.mktemp("db") / "assistant_test.db"
    url = f"sqlite:///{db_path}"
    os.environ["ASSISTANT_DATABASE_URL"] = url
    return url


@pytest.fixture(scope="session")
def app_client(test_database: str) -> Generator[TestClient, None, None]:
    from app.main import app
    from app.db.base import Base
    from app.db.session import engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as client:
        yield client


@pytest.fixture()
def db_session(test_database: str) -> Generator[Session, None, None]:
    engine = create_engine(test_database, future=True, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session, future=True)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
