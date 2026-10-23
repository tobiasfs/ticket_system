#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:09:31 2026
"""

from abc import ABC, abstractmethod

class SystemConfigPort(ABC):
    @abstractmethod
    def get_version(self) -> list[int]:
        pass

    @abstractmethod
    def get_enabled_features(self) -> set[str]:
        pass
