
cache = {}
cache_size = 5000


def add_cache(word, trans):
    if len(cache) > cache_size:
        cache.pop(cache.__iter__().__next__())

    cache[word] = trans


def get_cache(word):
    return cache.get(word, None)

