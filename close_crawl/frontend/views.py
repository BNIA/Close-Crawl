#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

from __future__ import absolute_import, print_function, unicode_literals
from datetime import datetime

from flask import request, render_template, redirect

from .config import app
from .context import modules
from modules import close_crawl_cli
from modules._version import __version__


@app.context_processor
def inject_version():
    return dict(ver=__version__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/scrape', methods=('GET', 'POST'))
def scrape():

    min_val = 1
    max_val = min_val + 500

    if request.method == "POST":

        close_crawl_cli.main(**request.form.to_dict())
        return redirect('/')

    return render_template(
        'scrape.html',
        min_val=min_val,
        max_val=max_val,
        current_year=xrange(datetime.now().year, 2009, -1)
    )


@app.route('/shutdown')
def shutdown():
    werkzeug_server = request.environ.get('werkzeug.server.shutdown')
    werkzeug_server()
    return 'Server shutting down...'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
