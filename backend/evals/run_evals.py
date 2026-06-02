import json
import time
import csv
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.graph.nodes import router_node


GOLDEN_FILE = "evals/golden_set.jsonl"
FAILURE_FILE = "evals/failure_cases.jsonl"
RESULTS_FILE = "evals/results.csv"

correct = 0
total = 0

latencies = []

with open(GOLDEN_FILE, "r") as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        item = json.loads(line)

        state = {
            "messages": [
                {
                    "role": "user",
                    "content": item["input"]
                }
            ]
        }

        start = time.time()

        result = router_node(state)

        latency = (
            time.time() - start
        ) * 1000

        latencies.append(latency)

        predicted = result["next_step"]

        if predicted == item["expected_route"]:
            correct += 1
        else:
            print()
            print("FAILED CASE")
            print("Input:", item["input"])
            print("Expected:", item["expected_route"])
            print("Predicted:", predicted)
            print()

        total += 1


router_accuracy = (
    correct / total
) * 100

avg_latency = (
    sum(latencies)
    / len(latencies)
)

latencies.sort()

p50_latency = latencies[
    int(len(latencies) * 0.50)
]

p95_latency = latencies[
    min(
        int(len(latencies) * 0.95),
        len(latencies) - 1
    )
]

failure_rate = (
    (total - correct)
    / total
) * 100

failure_cases = 0

with open(FAILURE_FILE, "r") as f:
    for line in f:
        if line.strip():
            failure_cases += 1


# Create CSV if it doesn't exist
results_path = Path(RESULTS_FILE)

if not results_path.exists():

    with open(
        RESULTS_FILE,
        "w",
        newline=""
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "date",
            "router_accuracy",
            "golden_cases",
            "failure_cases",
            "avg_latency_ms",
            "p50_latency_ms",
            "p95_latency_ms",
            "failure_rate"
        ])


# Append current run
with open(
    RESULTS_FILE,
    "a",
    newline=""
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        round(router_accuracy, 2),
        total,
        failure_cases,
        round(avg_latency, 2),
        round(p50_latency, 2),
        round(p95_latency, 2),
        round(failure_rate, 2)
    ])


print()
print("=" * 50)
print("ASTROAGENT EVALUATION REPORT")
print("=" * 50)
print()

print(
    f"Router Accuracy      : {router_accuracy:.2f}%"
)

print(
    f"Golden Set Cases     : {total}"
)

print(
    f"Failure Cases        : {failure_cases}"
)

print(
    f"Average Latency      : {avg_latency:.2f} ms"
)

print(
    f"P50 Latency          : {p50_latency:.2f} ms"
)

print(
    f"P95 Latency          : {p95_latency:.2f} ms"
)

print(
    f"Failure Rate         : {failure_rate:.2f}%"
)

print()
print(
    f"Results saved to     : {RESULTS_FILE}"
)

print()
print("=" * 50)