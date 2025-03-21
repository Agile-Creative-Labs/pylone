#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py - Pylone Web MVC Framework Server Runner

This script runs the Pylone web application server with configurable options.
It can run both HTTP and WebSocket servers or just the HTTP server.

Usage:
    python3 run.py                      # Run with default settings (HTTP: 8000, WS: 8001)
    python3 run.py -p 9000              # Run HTTP server on port 9000, WS on 8001
    python3 run.py -w 9001              # Run HTTP server on port 8000, WS on 9001
    python3 run.py --no-ws              # Run only HTTP server (no WebSocket)
    python3 run.py -p 9000 -w 9001      # Run HTTP on 9000, WS on 9001
    python3 run.py --debug              # Run with debug logging enabled
    python3 run.py --help-info          # Display detailed help information

Examples:
    Standard web server:      python run.py
    Custom ports:             python run.py -p 5000 -w 5001
    HTTP only:                python run.py --no-ws
    Development mode:         python run.py --debug -p 3000

Author: Agile Creative Labs Inc.
License: Apache License
Copyright: (c) 2025 Agile Creative Labs Inc
"""

import sys
import signal
import logging
import argparse
from demo.app import app

# Fancy Open-Source Banner
BANNER = r"""
   ____        __               
   / ** \**  **/ /**_  ____  ___ 
  / /_/ / / / / / ** \/ ** \/ _ \
 / ____/ /_/ / / /_/ / / / /  __/
/_/    \__, /_/\____/_/ /_/\___/ 
      /____/  
Pylone Framework v1.0 (c) 2025 Agile Creative Labs Inc
Apache License | Open Source & Free | Built with 🖖 by Starfleet Engineers
"""

# Detailed help information
HELP_INFO = """
Pylone Framework Server Runner - Detailed Help
==============================================

DESCRIPTION:
  The Pylone Framework provides a high-performance web server with built-in
  WebSocket support for real-time applications. This runner script allows you
  to configure and launch the server with various options.

REQUIREMENTS:
  - Python 3.8 or higher
  - demo.app module (part of Pylone Framework)

SERVER MODES:
  1. Full Mode (Default)
     - Runs both HTTP and WebSocket servers
     - Example: python run.py

  2. HTTP-Only Mode
     - Runs only the HTTP server, no WebSocket support
     - Example: python run.py --no-ws

PORT CONFIGURATION:
  - Valid port range: 1024-65535 (ports below 1024 require root/admin privileges)
  - HTTP and WebSocket ports must be different
  - Default HTTP port: 8000
  - Default WebSocket port: 8001

DEBUGGING:
  When --debug is enabled:
  - Detailed logging information is displayed
  - Log level is set to DEBUG instead of INFO
  - Useful for development and troubleshooting

RUNTIME CONTROLS:
  - Press CTRL+C to gracefully shutdown the server
  - The shutdown process will close all active connections properly

ADDITIONAL RESOURCES:
  - Documentation: https://docs.pylone-framework.org
  - GitHub: https://github.com/agilecreativelabs/pylone
  - Issue Tracker: https://github.com/agilecreativelabs/pylone/issues

Pylone Framework v1.0 (c) 2025 Agile Creative Labs Inc
Apache License | Open Source & Free
"""

# Command-line argument parser
parser = argparse.ArgumentParser(description="Run the Pylone web server.")
parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run the HTTP server on (default: 8000)")
parser.add_argument("-w", "--ws-port", type=int, default=8001, help="Port to run the WebSocket server on (default: 8001)")
parser.add_argument("--no-ws", action="store_true", help="Disable WebSocket server")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--help-info", action="store_true", help="Display detailed help information")
args = parser.parse_args()

# Display banner
print(BANNER)

# Check if help info was requested
if args.help_info:
    print(HELP_INFO)
    sys.exit(0)

# Setup logging
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level)

# Validate WebSocket port if WebSocket is enabled
if not args.no_ws:
    if args.ws_port < 1024 or args.ws_port > 65535:
        print(f"Error: WebSocket port {args.ws_port} is out of valid range (1024-65535)")
        sys.exit(1)
    
    # Check if HTTP and WebSocket ports are the same
    if args.port == args.ws_port:
        print(f"Error: HTTP port and WebSocket port cannot be the same ({args.port})")
        sys.exit(1)

# Handle CTRL+C to shutdown gracefully
def shutdown_server(signal, frame):
    print("\nCaptain, we are shutting down the server gracefully... 🖖")
    app.shutdown()  # Shutdown the WebSocket server
    sys.exit(0)

# Bind SIGINT (CTRL+C) to the shutdown function
signal.signal(signal.SIGINT, shutdown_server)

# Start the servers
if __name__ == '__main__':
    if args.no_ws:
        # Run only HTTP server if WebSocket is disabled
        print(f"Starting HTTP server on http://127.0.0.1:{args.port}")
        print(f"WebSocket server is disabled")
        app.run(http_host="127.0.0.1", http_port=args.port, ws_enabled=False)
    else:
        # Run both HTTP and WebSocket servers
        print(f"Starting HTTP server on http://127.0.0.1:{args.port}")
        print(f"Starting WebSocket server on ws://127.0.0.1:{args.ws_port}")
        app.run(http_host="127.0.0.1", http_port=args.port, ws_host="127.0.0.1", ws_port=args.ws_port)
        