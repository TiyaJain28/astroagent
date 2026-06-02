from fastapi import APIRouter

from app.models.chat_request import ChatRequest
from app.graph.graph import build_graph
from app.services.memory import get_profile
router = APIRouter()

graph = build_graph()

@router.post("/chat")
async def chat(request: ChatRequest):

    birth_details = get_profile(
        "default_user"
    )

    if birth_details is None:

        birth_details = {
            "date": request.date,
            "time": request.time,
            "place": request.place
        }

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            "birth_details": birth_details,
            "tool_output": {},
            "final_response": "",
            "next_step": ""
        }
    )

    return {
        "response": result["final_response"]
    }