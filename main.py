#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:06:24 2026

@author: toby
"""

import argparse
import logging
import sys
from src.infrastructure.configuation import Configuration
from src.application.web.web import start_web_services
from src.application.cli.cli import run_cli

logger = logging.getLogger()


def parse_commandline():
    """
    Parses the global flags. We use parse_known_args so that 
    command-line positional arguments (like 'projects show') 
    don't cause errors here.
    """
    parser = argparse.ArgumentParser(description="Issue Tracking System")
    parser.add_argument('--port', type=int, default=8080, help="Port for web services")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Host address")
    parser.add_argument('--mcp', action='store_true', help="Start MCP server")
    parser.add_argument('--web', action='store_true', help="Start Web Frontend")
    parser.add_argument('--rest', action='store_true', help="Start REST API")
    
    # parse_known_args returns (namespace, list_of_unparsed_args)
    return parser.parse_known_args()

def main():
    # 1. Load Configuration
    try:
        config = Configuration("config/system.ini")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # 2. Parse CLI Flags
    args, cli_args = parse_commandline()

    # 3. Merge Config with CLI arguments
    # CLI flags take precedence over .ini file
    server_config = config.get_server_config()
    port = args.port if args.port != 8080 else server_config['port']
    host = args.host if args.host != '127.0.0.1' else server_config['host']
    
    # Determine service activation (CLI flag OR ini file)
    features = config.get_feature_flags()
    mcp_active = args.mcp or features['mcp']
    web_active = args.web or features['web']
    rest_active = args.rest or features['rest']

    # 4. Logic: Prevent Web and CLI usage together
    is_web_service_running = mcp_active or web_active or rest_active
    is_cli_command_provided = len(cli_args) > 0

    if is_web_service_running and is_cli_command_provided:
        logger.error("Conflict: Cannot run Web Services and CLI commands simultaneously.")
        sys.exit(1)

    # 5. Dispatch
    if is_web_service_running:
        start_web_services(port, host, mcp_active, web_active, rest_active)
    elif is_cli_command_provided:
        run_cli(cli_args)
    else:
        logger.info("No command provided. Use --help for usage.")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Started")
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    logger.info("Finished")
