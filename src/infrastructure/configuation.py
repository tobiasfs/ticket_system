# -*- coding: utf-8 -*-

import configparser
import os

class Configuration:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")
        self.config.read(config_path)

    def get_server_config(self):
        return {
            "port": self.config.getint("server", "port", fallback=8080),
            "host": self.config.get("server", "host", fallback="127.0.0.1"),
        }

    def get_feature_flags(self):
        return {
            "mcp": self.config.getboolean("features", "mcp_enabled", fallback=False),
            "web": self.config.getboolean("features", "web_enabled", fallback=False),
            "rest": self.config.getboolean("features", "rest_enabled", fallback=False),
        }
