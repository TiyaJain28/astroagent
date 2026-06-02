import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.tools.birth_chart_tool import (
    compute_birth_chart
)
from app.tools.birth_chart_tool import (
    compute_birth_chart
)

chart = compute_birth_chart(
    "2000-01-01",
    "12:00",
    26.91,
    75.81
)

required = [
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Rahu",
    "Ketu",
    "Ascendant",
    "Houses"
]

missing = []

for item in required:

    if item not in chart:
        missing.append(item)

if not missing:
    print("Birth Chart Test: PASS")
else:
    print(
        "Missing:",
        missing
    )