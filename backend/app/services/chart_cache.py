_chart_cache = {}


def get_cached_chart(key):
    return _chart_cache.get(key)


def save_chart(key, chart):
    _chart_cache[key] = chart