from os import path
import string
from random import SystemRandom, uniform

from flask import Flask

BASE_DIR = path.dirname(path.abspath(__file__))
TEMPLATE_DIR = path.join(BASE_DIR, "templates")
STATIC_DIR = path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.secret_key = ''.join(
    SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for _ in range(int(uniform(10, 20)))
)
