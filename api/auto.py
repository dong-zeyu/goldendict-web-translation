import google as google
import youdao as youdao
from exceptions import TranslateException

cache = {}
cache_size = 5000


def get_trans(word):
    if word in cache:
        return cache[word]

    try:
        trans = youdao.get_trans(word, False)
    except TranslateException:
        trans = google.get_trans(word)

    if len(cache) > cache_size:
        cache.pop(cache.__iter__().__next__())

    cache[word] = trans

    return trans
