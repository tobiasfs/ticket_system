#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:06:02 2026

@author: toby
"""

import json
from typing import Optional

from flask import Blueprint, abort, jsonify, render_template, request
from jinja2 import TemplateNotFound

from .json_rpc import JSONRPCServer

mcp_blueprint = Blueprint("mcp", __name__)

rpc_server = JSONRPCServer()


@rpc_server.register("initialize")
def handle_initialize(
    protocolVersion: Optional[str] = None,
    capabilities: Optional[dict] = None,
    clientInfo: Optional[dict] = None,
):
    print(f"Requested protocolVersion: {protocolVersion}")

    # Notice how params are automatically mapped to function arguments!
    return {
        "protocolVersion": "2025-11-25",
        "capabilities": {
            "tools": {
                "listChanged": False,
                "resources": {
                    "listChanged": False,
                    "subscribe": False,
                },
            }
        },
        "serverInfo": {
            "name": "Ticket System",
            "version": "0.1.0",
        },
    }


@rpc_server.register("notifications/initialized")
def handle_notifications_initialized():
    print("MCP Client reports intitalization")
    return "OK"


@mcp_blueprint.route("/mcp", methods=["POST"])
def show():
    print(request.data.decode())

    x = json.loads(request.data.decode())

    if not isinstance(x, dict):
        abort(404)

    if "method" in x.keys():
        method = x["method"]
        print("Request received: " + method)

        result = rpc_server.handle(x)
        print("Result returned ------")
        print(json.dumps(result, indent=2))
        print("------")
        return jsonify(result)
