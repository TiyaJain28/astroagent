import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.graph.nodes import router_node
from app.graph.nodes import router_node

cases = [
    ("What does my chart say about career?", "birth_chart"),
    ("What is my energy today?", "daily_transit"),
    ("Hello", "general"),
]

passed = 0

for message, expected in cases:

    state = {
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    result = router_node(state)

    if result["next_step"] == expected:
        passed += 1

print(
    f"Tool Routing: {passed}/{len(cases)}"
)