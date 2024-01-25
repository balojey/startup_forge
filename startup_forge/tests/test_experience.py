from datetime import date
import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from sqlalchemy.sql import func

from startup_forge.db.dao.experience_dao import ExperienceDAO
from startup_forge.db.models.options import Role, Industry


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests experience instance creation."""

    url = fastapi_app.url_path_for("create_experience")
    company_name = uuid.uuid4().hex
    description = uuid.uuid4().hex
    start_date = "2015-07-21"
    industry = Industry.AI
    response = await authenticated_client.post(
        url,
        json={
            "company_name": company_name,
            "description": description,
            "start_date": start_date,
            "industry": industry,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    dao = ExperienceDAO(dbsession)
    instances = await dao.filter(company_name=company_name)
    assert instances[0].company_name == company_name


# @pytest.mark.anyio
# async def test_getting(
#     fastapi_app: FastAPI,
#     authenticated_client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests experience instance retrieval."""
#     url = fastapi_app.url_path_for("create_experience")
#     company_name = uuid.uuid4().hex
#     description = uuid.uuid4().hex
#     start_date = "2015-07-21"
#     industry = Industry.AI
#     response1 = await authenticated_client.post(
#         url,
#         json={
#             "company_name": company_name,
#             "description": description,
#             "start_date": start_date,
#             "industry": industry,
#         },
#     )
#     assert response1.status_code == status.HTTP_201_CREATED

#     dao = ExperienceDAO(dbsession)
#     instances = await dao.filter(company_name=company_name)
#     assert instances[0].company_name == company_name

#     url = fastapi_app.url_path_for("get_experience")
#     response = await authenticated_client.get(
#         url, params={"experience_id": instances[0].id}
#     )
#     experience = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert experience["company_name"] == company_name


# @pytest.mark.anyio
# async def test_getting_many(
#     fastapi_app: FastAPI,
#     authenticated_client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests experience instances retrieval."""
#     url1 = fastapi_app.url_path_for("create_experience")
#     company_name1 = uuid.uuid4().hex
#     description1 = uuid.uuid4().hex
#     start_date1 = "2015-07-21"
#     industry1 = Industry.AI
#     response1 = await authenticated_client.post(
#         url1,
#         json={
#             "company_name": company_name1,
#             "description": description1,
#             "start_date": start_date1,
#             "industry": industry1,
#         },
#     )
#     assert response1.status_code == status.HTTP_201_CREATED

#     url2 = fastapi_app.url_path_for("create_experience")
#     company_name2 = company_name1
#     description2 = uuid.uuid4().hex
#     start_date2 = "2025-07-22"
#     industry2 = Industry.FINTECH
#     response2 = await authenticated_client.post(
#         url2,
#         json={
#             "company_name": company_name2,
#             "description": description2,
#             "start_date": start_date2,
#             "industry": industry2,
#         },
#     )
#     assert response1.status_code == status.HTTP_201_CREATED

#     dao = ExperienceDAO(dbsession)
#     instances = await dao.filter(company_name=company_name1)
#     assert instances[0].company_name == company_name1

#     url = fastapi_app.url_path_for("get_experiences")
#     response = await authenticated_client.get(
#         url,
#     )
#     experience = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert len(experience) == 2


@pytest.mark.anyio
async def test_updating(
    fastapi_app: FastAPI,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests experience instance updating."""

    url = fastapi_app.url_path_for("create_experience")
    company_name = uuid.uuid4().hex
    description = uuid.uuid4().hex
    start_date = "2015-07-21"
    industry = Industry.AI
    response = await authenticated_client.post(
        url,
        json={
            "company_name": company_name,
            "description": description,
            "start_date": start_date,
            "industry": industry,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    dao = ExperienceDAO(dbsession)
    instances = await dao.filter(company_name=company_name)
    assert instances[0].company_name == company_name

    instance = instances[0]
    new_url = fastapi_app.url_path_for("update_experience")
    response = await authenticated_client.patch(
        new_url,
        json={"company_name": uuid.uuid4().hex},
        params={"experience_id": instance["id"]},
    )
    assert response.status_code == status.HTTP_200_OK


# @pytest.mark.anyio
# async def test_updating(
#     fastapi_app: FastAPI,
#     authenticated_client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests profile instance updating."""

#     url = fastapi_app.url_path_for("create_profile")
#     first_name = uuid.uuid4().hex
#     last_name = uuid.uuid4().hex
#     response = await authenticated_client.post(
#         url,
#         json={"first_name": first_name, "last_name": last_name, "role": Role.MENTEE},
#     )

#     assert response.status_code == status.HTTP_201_CREATED

#     url = fastapi_app.url_path_for("update_profile")
#     time = func.now()
#     response = await authenticated_client.patch(
#         url,
#         json={"role": Role.MENTOR},
#     )

#     assert response.status_code == status.HTTP_200_OK

#     dao = ProfileDAO(dbsession)
#     instances = await dao.filter(first_name=first_name)
#     assert instances[0].first_name == first_name
#     assert instances[0].last_name == last_name
#     assert instances[0].role == Role.MENTOR
#     # assert instances[0].updated_at <= time
