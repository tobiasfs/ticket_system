#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:23:24 2026

@author: Tobias Schaefer
"""

import logging
import uuid

from flask import Flask
from flask_cors import CORS

from src.application.use_cases.register import register_usecases
from src.infrastructure.configuration import Configuration

from .mcp import mcp_blueprint
from .rest import rest_blueprint
from .wui import wui_blueprint

logger = logging.getLogger(__name__)


class WebServer:
    def __init__(self, configuration: Configuration):

        server_config = configuration.get_server_config()

        self.port = server_config.get("port")
        self.host = server_config.get("host")

        self.app = Flask(__name__, static_folder="static")

        self.app.debug = server_config.get("debug")

        self.app.config.update(
            SESSION_COOKIE_SECURE=False,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",
        )
        self.app.secret_key = str(uuid.uuid4())

        self.app.config["USE_CASES"] = register_usecases(configuration)


        feature_config = configuration.get_feature_flags()
        self.add_services(feature_config)

    def run(self):
        print(str(self.app.url_map))
        logger.info(f"Initializing Web Services on {self.host}:{self.port}...")
        self.app.run(host=self.host, port=self.port)

    def add_services(self, config: dict):
        if config.get("mcp", False):
            logger.info("Starting MCP Server...")
            self.app.register_blueprint(mcp_blueprint)
            # Enable Cross-site-scriptiong ONLY for the mcp folder, so that
            # LLama.cpp et al can access the endpoint.
            CORS(self.app, resources={r"/mcp/?":{"origins":"*"}})

        if config.get("wui"):
            logger.info("Starting Flask Web Frontend...")
            self.app.register_blueprint(wui_blueprint)

        if config.get("rest"):
            logger.info("Starting REST API...")
            self.app.register_blueprint(rest_blueprint)
