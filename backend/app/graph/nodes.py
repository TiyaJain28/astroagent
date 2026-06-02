from app.state.astro_state import AstroState
from app.services.llm import get_llm
from app.services.chart_cache import (
    get_cached_chart,
    save_chart
)

from app.tools.geocode_tool import geocode_place
from app.tools.birth_chart_tool import compute_birth_chart
from app.tools.transit_tool import compute_daily_transits
from app.tools.knowledge_tool import knowledge_lookup


def router_node(state: AstroState):
    print("Router Node Executed")

    user_message = state["messages"][-1]["content"].lower()

    birth_chart_keywords = [
        "birth chart",
        "natal chart",
        "my chart",
        "chart",
        "relationships",
        "love life",
        "ascendant",
        "lagna",
        "personality"
    ]

    transit_keywords = [
        "today",
        "transit",
        "daily horoscope",
        "today's energy"
    ]

    if any(
        keyword in user_message
        for keyword in transit_keywords
    ):
        route = "daily_transit"

    elif any(
        keyword in user_message
        for keyword in birth_chart_keywords
    ):
        route = "birth_chart"

    else:
        route = "general"

    return {
        **state,
        "next_step": route
    }


def reasoning_node(state: AstroState):
    print("Reasoning Node Executed")

    return {
        **state,
        "next_step": "tool"
    }


def tool_node(state: AstroState):
    print("Tool Node Executed")

    birth_details = state["birth_details"]

    geo = geocode_place(
        birth_details["place"]
    )

    if not geo["success"]:
        return {
            **state,
            "tool_output": {
                "error": "Could not find birth place."
            }
        }

    cache_key = (
        f"{birth_details['date']}_"
        f"{birth_details['time']}_"
        f"{birth_details['place']}"
    )

    chart = get_cached_chart(
        cache_key
    )

    if chart is None:

        chart = compute_birth_chart(
            birth_details["date"],
            birth_details["time"],
            geo["latitude"],
            geo["longitude"]
        )

        save_chart(
            cache_key,
            chart
        )

        print("CACHE MISS")

    else:

        print("CACHE HIT")

    chart["BirthPlace"] = {
        "place": birth_details["place"],
        "latitude": geo["latitude"],
        "longitude": geo["longitude"]
    }

    return {
        **state,
        "tool_output": chart,
        "next_step": "end"
    }


def transit_node(state: AstroState):
    print("Transit Node Executed")

    birth_details = state["birth_details"]

    geo = geocode_place(
        birth_details["place"]
    )

    if not geo["success"]:
        return {
            **state,
            "tool_output": {
                "error": "Could not find birth place."
            }
        }

    cache_key = (
        f"{birth_details['date']}_"
        f"{birth_details['time']}_"
        f"{birth_details['place']}"
    )

    natal_chart = get_cached_chart(
        cache_key
    )

    if natal_chart is None:

        natal_chart = compute_birth_chart(
            birth_details["date"],
            birth_details["time"],
            geo["latitude"],
            geo["longitude"]
        )

        save_chart(
            cache_key,
            natal_chart
        )

        print("TRANSIT CACHE MISS")

    else:

        print("TRANSIT CACHE HIT")

    transits = compute_daily_transits(
        natal_chart
    )

    return {
        **state,
        "tool_output": {
            "natal_chart": natal_chart,
            "transits": transits
        },
        "next_step": "interpretation"
    }


def interpretation_node(state: AstroState):
    print("Interpretation Node Executed")

    llm = get_llm()

    chart = state.get(
        "tool_output",
        {}
    )

    question = state["messages"][-1]["content"]

    knowledge_query = question

    if isinstance(chart, dict):

        for planet, info in chart.items():

            if (
                isinstance(info, dict)
                and "sign" in info
            ):
                knowledge_query += (
                    f" {planet} {info['sign']}"
                )

    knowledge_context = knowledge_lookup(
        knowledge_query
    )

    print("=== KNOWLEDGE ===")
    print(knowledge_context)

    prompt = f"""
You are Aradhana, a warm and thoughtful astrology guide.

Astrological Data:
{chart}

Reference Knowledge:
{knowledge_context}

User Question:
{question}

Instructions:
- Use the reference knowledge whenever relevant.
- Ground interpretations in the provided astrology notes.
- Do not invent astrology meanings that conflict with the reference.
- Be warm and conversational.
- Never claim certainty.
- Never provide medical, legal, or financial guarantees.
- Keep the response under 250 words.
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "final_response": response.content
    }