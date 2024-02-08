from fastapi.routing import APIRouter

from startup_forge.web.api import (
    docs,
    profile,
    echo,
    monitoring,
    users,
    experience,
    mentor_mentee,
    education,
    community,
    connection,
    booking,
    review
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(experience.router, prefix="/experiences", tags=["experience"])
api_router.include_router(profile.router, prefix="/profiles", tags=["profile"])
api_router.include_router(mentor_mentee.router, prefix="/matches", tags=["match"])
api_router.include_router(education.router, prefix="/educations", tags=["educations"])
api_router.include_router(community.router, prefix="/communities", tags=["communities"])
api_router.include_router(connection.router, prefix="/connections", tags=["connections"])
api_router.include_router(booking.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(review.router, prefix="/reviews", tags=["reviews"])
