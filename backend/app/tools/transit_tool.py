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


def compute_daily_transits(natal_chart):
    now = datetime.utcnow()

    jd = swe.julday(
        now.year,
        now.month,
        now.day,
        now.hour + now.minute / 60.0
    )

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS
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

    # Compare transits with natal chart
    comparisons = {}

    for planet in [
        "Sun",
        "Moon",
        "Mercury",
        "Venus",
        "Mars"
    ]:

        if planet in natal_chart:

            comparisons[planet] = {
                "natal_sign": natal_chart[planet]["sign"],
                "transit_sign": result[planet]["sign"]
            }

    result["natal_comparison"] = comparisons

    return result