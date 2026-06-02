from fastapi import APIRouter
from app.models.birth_details import BirthDetails
from app.services.memory import save_profile

router = APIRouter()


@router.post("/birth")
async def save_birth_details(
    details: BirthDetails
):

    save_profile(
        "default_user",
        {
            "date": details.date,
            "time": details.time,
            "place": details.place
        }
    )

    return {
        "message": "Birth details saved",
        "data": details
    }