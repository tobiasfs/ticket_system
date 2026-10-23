#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:38:29 2026

@author: toby
"""

from src.domain.port.configuration.system_info import SystemConfigPort

class GetSystemInfoUseCase:
    def __init__(self, config_port: SystemConfigPort):
        self.config_port = config_port

    def execute(self):
        # Logic: orchestrate getting the version
        version = self.config_port.get_version()
        features = self.config_port.get_enabled_features()
        return {"version": version, "features": features}
