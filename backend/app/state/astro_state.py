from typing import TypedDict, List, Dict, Any


class AstroState(TypedDict):
    messages: List[dict]
    birth_details: Dict[str, Any]
    tool_output: Dict[str, Any]
    final_response: str
    next_step: str