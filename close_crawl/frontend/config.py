#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

from os import path
import string
from random import SystemRandom, uniform

from flask import Flask

# extra modules to manually add hooks for building executible
# TODO: fix this
from .extra_mods import *

BASE_DIR = path.dirname(path.abspath(__file__))
TEMPLATE_DIR = path.join(BASE_DIR, "templates")
STATIC_DIR = path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.secret_key = ''.join(
    SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for _ in range(int(uniform(10, 20)))
)
