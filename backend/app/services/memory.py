import json
from pathlib import Path

MEMORY_FILE = "data/user_profiles.json"


def load_profiles():

    path = Path(MEMORY_FILE)

    if not path.exists():
        return {}

    with open(path, "r") as f:
        return json.load(f)


def save_profile(user_id, profile):

    profiles = load_profiles()

    profiles[user_id] = profile

    Path("data").mkdir(
        exist_ok=True
    )

    with open(MEMORY_FILE, "w") as f:
        json.dump(
            profiles,
            f,
            indent=2
        )


def get_profile(user_id):

    profiles = load_profiles()

    return profiles.get(user_id)