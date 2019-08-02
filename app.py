import logging
import sys
from exceptions import TranslateException

import flask
from flask import Flask, abort, render_template, request

sys.path.append("./api")
app = Flask(__name__)


@app.route('/translate')
def index():
    word = request.args.get("q")
    serv = request.args.get("s", "auto")
    try:
        module = __import__(serv)
        if not hasattr(module, "get_trans"):
            raise ImportError("No avalible api [get_trans] found")
        return render_template(
            'index.html', word=word, trans=module.get_trans(word))
    except ImportError as e:
        logging.warn("Import Module [%s] Failed: %s", serv, e)
        return render_template(
            'index.html',
            word="Error",
            trans=[f"Import Module [{serv}] Failed"]), 500
    except TranslateException:
        return render_template(
            'index.html',
            word="Error",
            trans=[f"Faid to translate [{word}]"]), 500


if __name__ == '__main__':
    app.run(debug=True)
