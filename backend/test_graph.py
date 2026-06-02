from app.graph.graph import build_graph

graph = build_graph()

result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What does my chart say about my career?"
            }
        ],
        "birth_details": {
            "date": "2000-01-01",
            "time": "12:00",
            "place": "Delhi"
        },
        "tool_output": {},
        "final_response": "",
        "next_step": ""
    }
)

print(result["final_response"])