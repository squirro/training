#!/opt/squirro/virtualenv/bin/python

'''
This is a template for a flask app
'''

import time
import os
import site
import sys
import urllib
import requests
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request, Response, render_template, jsonify, send_from_directory

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET'])
def fetch():
    """Main Route that displays the documentation"""

    return jsonify({"Hello": "World!"})

if __name__ == "__main__":
    app.run(port=8181, debug=True)
