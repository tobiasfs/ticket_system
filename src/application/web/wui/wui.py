# -*- coding: utf-8 -*-

import os

from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound

wui_blueprint = Blueprint("wui", __name__, template_folder="../templates")

# @wui_blueprint.route("/css/<filename>")
# def serve_css(filename: str):
#    return render_template('common/base.html')


@wui_blueprint.route("/")
def show():
    return render_template("common/base.html")
