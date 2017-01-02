import string
from random import SystemRandom, uniform

from flask import Flask

app = Flask(__name__)

app.secret_key = ''.join(
    SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for _ in range(int(uniform(10, 20)))
)
