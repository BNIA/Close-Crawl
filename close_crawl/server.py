from __future__ import absolute_import, print_function, unicode_literals

from flask import Flask, request, render_template, redirect
from forms import ScrapeForm

app = Flask(__name__)
app.secret_key = "fhdsbfdsnjfbj"


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/scrape', methods=('GET', 'POST'))
def scrape():

    form = ScrapeForm()
    min_val = 4
    max_val = 500 + min_val

    if request.method == "POST":

        form_data = {
            key: value[0] for key, value in dict(request.form).items()
        }

        form_data["lower_bound"], form_data["upper_bound"] = \
            form_data["case_range"].split(',')
        del form_data["case_range"]
        print(form_data)

        return redirect('/')

    return render_template('scrape.html', form=form,
                           min_val=min_val, max_val=max_val)


def shutdown_server():

    werkzeug_server = request.environ.get('werkzeug.server.shutdown')
    if not werkzeug_server:
        raise RuntimeError('Not running with the Werkzeug Server')

    werkzeug_server()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':

    app.run(debug=True)
