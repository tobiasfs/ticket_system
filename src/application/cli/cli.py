#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:06:10 2026

@author: toby
"""
import argparse
import logging

logger = logging.getLogger(__name__)

def handle_projects(subparsers):
    project_parser = subparsers.add_parser("projects")
    project_subparsers = project_parser.add_subparsers(dest="project_command")
    # 'projects show'
    project_subparsers.add_parser("show")

def handle_issues(subparsers):
    issue_parser = subparsers.add_parser("issues")
    issue_subparsers = issue_parser.add_subparsers(dest="issue_command")
    
    # 'issues search jql="..."'
    search_parser = issue_subparsers.add_parser("search")
    search_parser.add_argument("jql", type=str)

    # 'issue ABC-123 set assignee marcus'
    # Note: This handles the singular 'issue' command mentioned in your prompt
    issue_parser.add_parser("set_status") # Simplified for example

def run_cli(args_list):
    """
    Takes the list of command line arguments (excluding the main script name)
    and processes them.
    """
    parser = argparse.ArgumentParser(prog="main.py")
    subparsers = parser.add_subparsers(dest="command")

    # Setup the command structure
    handle_projects(subparsers)
    handle_issues(subparsers)
    
    # Add the specific 'issue <id> set ...' logic
    # Because this is highly variable, we handle it as a generic command 
    # or via more complex subparsers.
    issue_cmd_parser = subparsers.add_parser("issue")
    issue_cmd_parser.add_argument("issue_id")
    issue_cmd_parser.add_argument("action")
    issue_cmd_parser.add_argument("target")

    try:
        # args_list is the remaining positional arguments from main.py
        parsed_args = parser.parse_args(args_list)
        
        if parsed_args.command == "projects":
            logger.info(f"Executing Projects Command: {parsed_args.project_command}")
        elif parsed_args.command == "issues":
            logger.info(f"Executing Issues Search: {parsed_args.jql}")
        elif parsed_args.command == "issue":
            logger.info(f"Updating {parsed_args.issue_id}: {parsed_args.action} {parsed_args.target}")
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"CLI Error: {e}")
