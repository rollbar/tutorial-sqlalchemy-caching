from typing import Generator

import pytest
from sqlalchemy import create_engine, engine, orm

from caching_tutorial import db, models


def pytest_addoption(parser):
    parser.addoption(
        "--echo-sql", action="store_true", default=False, help="Echo SQL queries"
    )


@pytest.fixture(scope="session")
def connection(request) -> Generator[engine.Connection, None, None]:
    engine = create_engine(
        "sqlite:///:memory:", echo=request.config.getoption("--echo-sql")
    )
    models.Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture(scope="function")
def session(connection: engine.Connection) -> Generator[orm.scoped_session, None, None]:
    session = orm.scoped_session(lambda: db.Session(bind=connection))
    try:
        yield session
    finally:
        session.rollback()


@pytest.fixture(scope="session")
def setup_db(connection: engine.Connection) -> Generator[None, None, None]:
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()

    yield

    models.Base.metadata.drop_all()
