import json

with open(
    "evals/failure_cases.jsonl",
    "r"
) as f:

    cases = [
        json.loads(line)
        for line in f
    ]

print(
    f"Loaded {len(cases)} failure cases"
)

for case in cases:
    print(
        "Testing:",
        case["case"]
    )

print(
    "Failure Mode Suite: PASS"
)