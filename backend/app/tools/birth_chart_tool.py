import swisseph as swe
from datetime import datetime


def get_zodiac_sign(longitude):
    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces"
    ]

    return signs[int(longitude // 30)]


def compute_birth_chart(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float
):
    dt = datetime.strptime(
        f"{date_str} {time_str}",
        "%Y-%m-%d %H:%M"
    )

    jd = swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0
    )

    # House system + Ascendant
    cusps, ascmc = swe.houses(
        jd,
        latitude,
        longitude,
        b'P'
    )

    ascendant = ascmc[0]

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE
    }

    result = {}

    for name, planet in planets.items():

        position = swe.calc_ut(
            jd,
            planet
        )[0]

        planet_longitude = round(
            position[0],
            2
        )

        result[name] = {
            "longitude": planet_longitude,
            "sign": get_zodiac_sign(
                planet_longitude
            )
        }

    # Ketu
    rahu_longitude = result["Rahu"]["longitude"]

    ketu_longitude = (
        rahu_longitude + 180
    ) % 360

    result["Ketu"] = {
        "longitude": round(
            ketu_longitude,
            2
        ),
        "sign": get_zodiac_sign(
            ketu_longitude
        )
    }

    # Ascendant (Lagna)
    result["Ascendant"] = {
        "longitude": round(
            ascendant,
            2
        ),
        "sign": get_zodiac_sign(
            ascendant
        )
    }

    # Houses
    houses_data = {}

    for i in range(12):

        house_longitude = round(
            cusps[i],
            2
        )

        houses_data[f"House_{i+1}"] = {
            "longitude": house_longitude,
            "sign": get_zodiac_sign(
                house_longitude
            )
        }

    result["Houses"] = houses_data

    return result