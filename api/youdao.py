import logging
import time
from exceptions import TranslateException
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

session = requests.session()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_trans(word, machine=True):
    try:
        count = 0
        while True:
            if count > 3:
                raise Exception("Maximum number of retries Exceeded")
            try:
                with session.get(
                        f"https://www.youdao.com/w/{quote(word)}/",
                        timeout=5) as re:
                    if re.status_code == 200:
                        content = BeautifulSoup(re.content.decode(),
                                                "html5lib")
                        trans = content.find(attrs={"id": "phrsListTab"})
                        if trans:
                            trans = trans.find(attrs={
                                "class": "trans-container"
                            }).find_all("li")
                            if trans:
                                trans = [i.text for i in trans]
                            else:
                                raise TranslateException(
                                    "No translation found")
                        elif machine:
                            trans = [
                                content.find(attrs={
                                    "id": "fanyiToggle"
                                }).find_all("p")[1].text
                            ]
                        else:
                            raise TranslateException("No translation found")
                        return trans
            except requests.RequestException:
                logger.warn(
                    "Network error when translating [%s]: %s times remain",
                    word, count)
            count = count + 1
    except TranslateException as e:
        raise e
    except Exception as e:
        logger.warn("Faid to translate [%s]: %s", word, e, exc_info=True)
        raise TranslateException()
