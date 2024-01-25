import uuid
from typing import Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.utils import create_database, drop_database
from startup_forge.db.models.profile import Profile
from startup_forge.db.models.options import Role
from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.settings import settings
from startup_forge.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from startup_forge.db.meta import meta  # noqa: WPS433
    from startup_forge.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


# =====================================================================================


@pytest.fixture
async def authenticated_client(fastapi_app: FastAPI, client: AsyncClient):
    """
    Create an authenticated client by adding the authentication token to the headers.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    register_url = fastapi_app.url_path_for("register:register")
    register_response = await client.post(
        register_url,
        json={
            "email": "test@email.com",
            "password": "school",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )
    login_url = fastapi_app.url_path_for("auth:jwt.login")
    login_response = await client.post(
        login_url,
        data={
            "grant_type": "",
            "username": "test@email.com",
            "password": "school",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    client.headers.update(
        {
            "Authorization": f"{login_response.json()['token_type']} {login_response.json()['access_token']}"
        }
    )
    return client


@pytest.fixture
async def authenticated_client2(fastapi_app: FastAPI, client: AsyncClient):
    """
    Create an authenticated client by adding the authentication token to the headers.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    register_url = fastapi_app.url_path_for("register:register")
    register_response = await client.post(
        register_url,
        json={
            "email": "test2@email.com",
            "password": "school",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )
    login_url = fastapi_app.url_path_for("auth:jwt.login")
    login_response = await client.post(
        login_url,
        data={
            "grant_type": "",
            "username": "test2@email.com",
            "password": "school",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    client.headers.update(
        {
            "Authorization": f"{login_response.json()['token_type']} {login_response.json()['access_token']}"
        }
    )
    return client


@pytest.fixture
async def authenticated_client3(fastapi_app: FastAPI, client: AsyncClient):
    """
    Create an authenticated client by adding the authentication token to the headers.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    register_url = fastapi_app.url_path_for("register:register")
    register_response = await client.post(
        register_url,
        json={
            "email": "test3@email.com",
            "password": "school",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )
    login_url = fastapi_app.url_path_for("auth:jwt.login")
    login_response = await client.post(
        login_url,
        data={
            "grant_type": "",
            "username": "test3@email.com",
            "password": "school",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    client.headers.update(
        {
            "Authorization": f"{login_response.json()['token_type']} {login_response.json()['access_token']}"
        }
    )
    return client


@pytest.fixture
async def mentor_profile(
    authenticated_client: AsyncClient, dbsession: AsyncSession, fastapi_app: FastAPI
) -> Profile:
    """
    Create a mentor profile.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    url = fastapi_app.url_path_for("create_profile")
    first_name = uuid.uuid4().hex
    last_name = uuid.uuid4().hex
    response = await authenticated_client.post(
        url,
        json={
            "first_name": first_name,
            "last_name": last_name,
            "role": Role.MENTOR,
        },
    )

    dao = ProfileDAO(dbsession)
    instances = await dao.filter(first_name=first_name)

    return instances[0]


@pytest.fixture
async def mentor_profile2(
    authenticated_client2: AsyncClient, dbsession: AsyncSession, fastapi_app: FastAPI
) -> Profile:
    """
    Create a mentor profile.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    url = fastapi_app.url_path_for("create_profile")
    first_name = uuid.uuid4().hex
    last_name = uuid.uuid4().hex
    response = await authenticated_client2.post(
        url,
        json={
            "first_name": first_name,
            "last_name": last_name,
            "role": Role.MENTOR,
        },
    )

    dao = ProfileDAO(dbsession)
    instances = await dao.filter(first_name=first_name)

    return instances[0]


@pytest.fixture
async def mentor_profile3(
    authenticated_client3: AsyncClient, dbsession: AsyncSession, fastapi_app: FastAPI
) -> Profile:
    """
    Create a mentor profile.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    url = fastapi_app.url_path_for("create_profile")
    first_name = uuid.uuid4().hex
    last_name = uuid.uuid4().hex
    response = await authenticated_client3.post(
        url,
        json={
            "first_name": first_name,
            "last_name": last_name,
            "role": Role.MENTOR,
        },
    )

    dao = ProfileDAO(dbsession)
    instances = await dao.filter(first_name=first_name)

    return instances[0]


@pytest.fixture
async def mentee_profile(
    authenticated_client: AsyncClient, dbsession: AsyncSession, fastapi_app: FastAPI
) -> Profile:
    """
    Create a mentor profile.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    url = fastapi_app.url_path_for("create_profile")
    first_name = uuid.uuid4().hex
    last_name = uuid.uuid4().hex
    response = await authenticated_client.post(
        url,
        json={
            "first_name": first_name,
            "last_name": last_name,
            "role": Role.MENTEE,
        },
    )

    dao = ProfileDAO(dbsession)
    instances = await dao.filter(first_name=first_name)

    return instances[0]


@pytest.fixture
async def mentee_profile(
    authenticated_client2: AsyncClient, dbsession: AsyncSession, fastapi_app: FastAPI
) -> Profile:
    """
    Create a mentor profile.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    url = fastapi_app.url_path_for("create_profile")
    first_name = uuid.uuid4().hex
    last_name = uuid.uuid4().hex
    response = await authenticated_client2.post(
        url,
        json={
            "first_name": first_name,
            "last_name": last_name,
            "role": Role.MENTEE,
        },
    )

    dao = ProfileDAO(dbsession)
    instances = await dao.filter(first_name=first_name)

    return instances[0]


@pytest.fixture
async def mentee_profile(
    authenticated_client3: AsyncClient, dbsession: AsyncSession, fastapi_app: FastAPI
) -> Profile:
    """
    Create a mentor profile.

    :param fastapi_app: the application.
    :yield: client for the app.
    """

    url = fastapi_app.url_path_for("create_profile")
    first_name = uuid.uuid4().hex
    last_name = uuid.uuid4().hex
    response = await authenticated_client3.post(
        url,
        json={
            "first_name": first_name,
            "last_name": last_name,
            "role": Role.MENTEE,
        },
    )

    dao = ProfileDAO(dbsession)
    instances = await dao.filter(first_name=first_name)

    return instances[0]
