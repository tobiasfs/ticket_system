#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:06:38 2026

@author: Tobias Schaefer
"""

from flask import Blueprint, abort, jsonify, render_template, request
from jinja2 import TemplateNotFound
import datetime

rest_blueprint = Blueprint("rest", __name__)


@rest_blueprint.route("/rest/api/serverInfo", defaults={"version": "latest"})
@rest_blueprint.route("/rest/api/<version>/serverInfo")
def serverinfo(version):
    response = {
        "baseUrl": request.url_root,
        "buildDate": "?",
        "buildNumber": 0,
        "defaultLocale": {"locale": "en"},
        "displayUrl": request.url_root,
        "displayUrlConfluence": request.url_root,
        "displayUrlServicedeskHelpCenter": request.url_root,
        "scmInfo": "?",
        "serverTime": str(datetime.datetime.now()),
        "serverTimeZone": "?",
        "serverTitle": "?",
        "version": "?",
        "versionNumbers": [0, 1, 0],
    }
    return jsonify(response)
