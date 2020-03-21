import logging
from exceptions import TranslateException
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

session = requests.session()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_trans(word, machine=True):
    try:
        count = 3
        while True:
            if count == 0:
                raise TranslateException("Maximum number of retries Exceeded")
            try:
                with session.get(
                        f"https://www.youdao.com/w/{quote(word)}/",
                        timeout=2) as re:
                    if re.status_code == 200:
                        content = BeautifulSoup(re.content.decode(), "html5lib")
                        trans = content.find(id="phrsListTab")
                        trans = trans.find(attrs={
                            "class": "trans-container"
                        }) if trans else None
                        trans = trans.find_all("li") if trans else None

                        if trans:
                            return [i.text for i in trans]
                        elif machine:
                            # Try "网络释义" first
                            trans = content.find(id="tWebTrans")
                            trans = trans.find_all(attrs={
                                "class": "wt-container"
                            }) if trans else None

                            if trans:
                                return [
                                    i.find(attrs={
                                        "class": "title"
                                    }).find("span").text for i in trans
                                ]

                            # Try "机器翻译" then
                            trans = content.find(id="fanyiToggle")
                            if trans:
                                return [
                                    trans.find_all("p")[1].text
                                ]

                        raise TranslateException("No translation found")
            except requests.RequestException:
                count = count - 1
                logger.warn(
                    "Network error when translating [%s]: %s times remain",
                    word, count)
    except TranslateException as e:
        raise e
    except Exception as e:
        logger.warn("Faid to translate [%s]: %s", word, e, exc_info=True)
        raise TranslateException()
