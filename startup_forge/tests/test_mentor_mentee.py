# import uuid

# import pytest
# from fastapi import FastAPI
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status

# from sqlalchemy.sql import func

# from startup_forge.db.dao.mentor_mentee_dao import MentorMenteeDAO
# from startup_forge.db.models.profile import Profile
# from startup_forge.db.models.options import Role, Industry


# @pytest.mark.anyio
# async def test_creation(
#     fastapi_app: FastAPI,
#     authenticated_client: AsyncClient,
#     authenticated_client3: AsyncClient,
#     authenticated_client2: AsyncClient,
#     mentor_profile: Profile,
#     mentor_profile3: Profile,
#     mentee_profile2: Profile,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests match request."""

#     url = fastapi_app.url_path_for("create_experience")
#     response = await authenticated_client.post(
#         url,
#         json={
#             "company_name": uuid.uuid4().hex,
#             "start_date": "2002-07-12",
#             "end_date": "2010-12-20",
#             "industry": Industry.DIGITAL_MEDIA,
#         },
#     )
#     response2 = await authenticated_client3.post(
#         url,
#         json={
#             "company_name": uuid.uuid4().hex,
#             "start_date": "2008-07-12",
#             "industry": Industry.FINTECH,
#         },
#     )
#     response3 = await authenticated_client2.post(
#         url,
#         json={
#             "company_name": uuid.uuid4().hex,
#             "start_date": "2020-07-12",
#             "industry": Industry.CYBERSECURITY,
#         },
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response2.status_code == status.HTTP_201_CREATED
#     assert response3.status_code == status.HTTP_201_CREATED
    
#     url = fastapi_app.url_path_for("request_matches")
#     response = await authenticated_client3.get(url)
#     assert len(response.json()) == 0


# @pytest.mark.anyio
# async def test_getting(
#     fastapi_app: FastAPI,
#     authenticated_client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests profile instance retrieval."""
#     url1 = fastapi_app.url_path_for("create_profile")
#     first_name = uuid.uuid4().hex
#     last_name = uuid.uuid4().hex
#     response1 = await authenticated_client.post(
#         url1,
#         json={"first_name": first_name, "last_name": last_name, "role": Role.MENTEE},
#     )
#     url = fastapi_app.url_path_for("get_profile")
#     response = await authenticated_client.get(url)
#     profile = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert profile["first_name"] == first_name


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
