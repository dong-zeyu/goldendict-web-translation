import logging
from exceptions import TranslateException

import requests
from googletrans import Translator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
translator = Translator(
    service_urls=["translate.google.cn"],
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    timeout=5)


def get_trans(word, machine=True):
    try:
        dt = translator.detect(word)
        if dt.lang == "zh-CN":
            trans = translator.translate(word, dest="en")
        else:
            trans = translator.translate(word, dest="zh-CN")

        data = trans.extra_data
        if data["all-translations"]:
            trans = [
                f"{i[0]}: {'; '.join(i[1])}" for i in data["all-translations"]
            ]
        else:
            trans = [trans.text]

        return trans
    except requests.RequestException:
        logger.warn("Network error when translating [%s]", word)
        raise TranslateException()
    except Exception as e:
        logger.warn("Failed to translate [%s]: %s", word, e, exc_info=True)
        raise TranslateException()
