from fastapi.routing import APIRouter

from startup_forge.web.api import (
    docs,
    profile,
    echo,
    monitoring,
    users,
    experience,
    mentor_mentee,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(experience.router, prefix="/experiences", tags=["experience"])
api_router.include_router(profile.router, prefix="/profiles", tags=["profile"])
api_router.include_router(mentor_mentee.router, prefix="/matches", tags=["match"])
