from __future__ import absolute_import, print_function, unicode_literals
from flask import request, render_template, redirect

from .config import app
from .context import modules  # pylint: disable=unused-import
from modules import close_crawl_cli


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

    return render_template('scrape.html', min_val=min_val, max_val=max_val)


def shutdown_server():

    werkzeug_server = request.environ.get('werkzeug.server.shutdown')
    if not werkzeug_server:
        raise RuntimeError('Not running with the Werkzeug Server')

    werkzeug_server()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
