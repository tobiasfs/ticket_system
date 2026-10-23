#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:15:08 2026

@author: toby
"""

import functools
import json
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


class JSONRPCError(Exception):
    """Custom exception to pass specific RPC error codes."""

    def __init__(self, code: str, message: str, data: Optional[Any] = None) -> None:
        self.code: str = code
        self.message: str = message
        self.data: Optional[Any] = data


class JSONRPCServer:
    def __init__(self) -> None:

        # Maps method names to callable functions
        self.methods: dict[str, Any] = {}

        # Standard JSON-RPC 2.0 error codes
        self.ERRORS = {
            "PARSE_ERROR": {
                "code": -32700,
                "message": "Parse error",
            },
            "INVALID_REQUEST": {
                "code": -32600,
                "message": "Invalid Request",
            },
            "METHOD_NOT_FOUND": {
                "code": -32601,
                "message": "Method not found",
            },
            "INVALID_PARAMS": {
                "code": -32602,
                "message": "Invalid params",
            },
            "INTERNAL_ERROR": {
                "code": -32603,
                "message": "Internal error",
            },
        }

    def register(self, name: str):
        """Registers a function to a method name."""

        def decorator(func: Callable[..., T]):
            @functools.wraps(func)
            def wrapper(*args, **kvargs):
                return func(*args, **kvargs)

            self.methods[name] = wrapper
            return wrapper

        return decorator

    def _format_error(self, error_key, request_id=None, data=None):
        err = self.ERRORS.get(error_key, self.ERRORS["INTERNAL_ERROR"]).copy()
        if data is not None:
            err["data"] = data
        return {"jsonrpc": "2.0", "error": err, "id": request_id}

    def _format_result(self, result, request_id):
        return {"jsonrpc": "2.0", "result": result, "id": request_id}

    def _execute_method(self, method_name, params, request_id):
        """Internal dispatcher to call the registered function."""
        if method_name not in self.methods:
            return self._format_error(
                "METHOD_NOT_FOUND", request_id, data=str(method_name)
            )

        func = self.methods[method_name]
        try:
            # Handle both positional [1,2,3] and keyword {"a":1} params
            if isinstance(params, list):
                result = func(*params)
            elif isinstance(params, dict):
                result = func(**params)
            else:
                # If params is neither, treat as no params or invalid
                result = func()

            return self._format_result(result, request_id)

        except TypeError as e:
            return self._format_error("INVALID_PARAMS", request_id, data=str(e))
        except Exception as e:
            return self._format_error("INTERNAL_ERROR", request_id, data=str(e))

    def handle(self, raw_input):
        """
        The main entry point.
        Takes a JSON string or dict and returns a JSON response string.
        """
        try:
            if isinstance(raw_input, str):
                request = json.loads(raw_input)
            else:
                request = raw_input
        except json.JSONDecodeError as e:
            return self._format_error("PARSE_ERROR", data=str(e))

        # 1. Handle Batch Requests (List of requests)
        if isinstance(request, list):
            responses = []
            for req in request:
                resp = self._process_single_request(req)
                if resp:  # Notifications don't return anything
                    responses.append(resp)
            return responses if responses else None

        # 2. Handle Single Request
        return self._process_single_request(request)

    def _process_single_request(self, req):
        """Processes an individual JSON-RPC object."""
        # Validate basic structure
        if (
            not isinstance(req, dict)
            or req.get("jsonrpc") != "2.0"
            or "method" not in req
        ):
            return self._format_error(
                "INVALID_REQUEST",
                req.get("id") if isinstance(req, dict) else None,
            )

        method_name = req["method"]
        params = req.get("params", None)
        request_id = req.get("id")  # Can be None for notifications

        # Execute the method
        response = self._execute_method(method_name, params, request_id)

        # print(json.dumps(response, indent=2))

        # Notifications (no ID) should not return a response
        if request_id is None:
            return None

        return response
