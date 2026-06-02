from pathlib import Path


KNOWLEDGE_PATH = Path(
    "knowledge/astrology_notes.txt"
)


def knowledge_lookup(query: str):

    with open(
        KNOWLEDGE_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        knowledge = f.read()

    query_words = query.lower().split()

    matches = []

    for line in knowledge.split("\n"):

        if any(
            word in line.lower()
            for word in query_words
        ):
            matches.append(line)

    return "\n".join(matches[:15])