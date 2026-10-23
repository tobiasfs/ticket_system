# -*- coding: utf-8 -*-

import configparser
import logging
import os
import tomllib

logger = logging.getLogger(__name__)


class Configuration:
    def __init__(self, *args: str):
        self.config = None
        self.data = None
        for filename in args:
            [_, ext] = os.path.splitext(filename)
            if ext.lower() == ".ini":
                self.config = configparser.ConfigParser()
                if not os.path.exists(filename):
                    raise FileNotFoundError(f"Config file not found at {filename}")
                self.config.read(filename)
            elif ext.lower() == ".toml":
                with open(filename, "rb") as f:
                    self.data = tomllib.load(f)
            else:
                raise RuntimeError("Unknown config file type: " + filename)

    def get_project_info(self) -> dict:
        if not self.data:
            logger.warning("pyproject.toml not found, assuming defaults.")
            return {
                "name": "?",
            }
        project = self.data.get("project", None)
        if not project:
            logger.warning("pyproject.toml not found, assuming defaults.")
            return {
                "name": "?",
            }
        return {
            "name": project.get("name", "?"),
        }

    def get_server_config(self) -> dict:
        if not self.config:
            logger.warning("Configuration file not found, assuming defaults.")
            return {"port": 8080, "host": "127.0.0.1"}
        return {
            "port": self.config.getint("server", "port", fallback=8080),
            "host": self.config.get("server", "host", fallback="127.0.0.1"),
            "debug": self.config.getboolean("server", "debug", fallback=False),
        }

    def get_feature_flags(self) -> dict:
        if not self.config:
            logger.warning("Configuration file not found, assuming defaults.")
            return {"mcp": False, "wui": False, "rest": False}
        return {
            "mcp": self.config.getboolean("features", "mcp_enabled", fallback=False),
            "wui": self.config.getboolean("features", "wui_enabled", fallback=False),
            "rest": self.config.getboolean("features", "rest_enabled", fallback=False),
        }
