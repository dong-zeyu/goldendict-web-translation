import sys
import importlib
from flask import Flask, render_template, request

from .exceptions import TranslateException

app = Flask(__package__)
logger = app.logger


@app.route('/translate')
def index():
    word = request.args.get("q")
    serv = request.args.get("s", "auto")

    if not word:
        return render_template(
            'index.html',
            word="Error",
            trans=[f"No word provided"]), 400

    try:
        module = importlib.import_module(f".api.{serv}", package=__package__)
        if not hasattr(module, "get_trans"):
            raise ImportError("No available api [get_trans] found")
        return render_template(
            'index.html', word=word, trans=module.get_trans(word))
    except ImportError as e:
        logger.warn("Import Module [%s] Failed: %s", serv, e)
        return render_template(
            'index.html',
            word="Error",
            trans=[f"Import Module [{serv}] Failed"]), 500
    except TranslateException:
        return render_template(
            'index.html',
            word="Error",
            trans=[f"Faid to translate [{word}]"]), 500

