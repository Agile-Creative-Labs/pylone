"""
Filename: run.py

Description:
This script launches a web server using the Pylone Framework. It includes:
- A fancy open-source banner showcasing version and licensing details.
- Command-line argument parsing for customizable server configurations (e.g., HTTP and WebSocket ports, debug mode).
- Logging configuration based on the selected mode (info or debug).
- Signal handling for clean server shutdown upon receiving a termination signal (e.g., CTRL+C).

Features:
- Graceful shutdown mechanism for both HTTP and WebSocket servers.
- Extensible and customizable framework setup using `demo.app`.

Usage:
Run this script to start the Pylone HTTP server. Use command-line options to specify port numbers or enable debug mode:
    python your_script_name.py --port 8000 --ws-port 8001 --debug
"""

import sys
import signal
import logging
import argparse
from demo.app import app

# Fancy Open-Source Banner
BANNER = r"""
   ____        __               
   / __ \__  __/ /___  ____  ___ 
  / /_/ / / / / / __ \/ __ \/ _ \
 / ____/ /_/ / / /_/ / / / /  __/
/_/    \__, /_/\____/_/ /_/\___/ 
      /____/  
Pylone Framework v1.0 (c) 2025 Agile Creative Labs Inc
Apache License | Open Source & Free | Built with 🖖 by Starfleet Engineers
"""

print(BANNER)

# Command-line argument parser
parser = argparse.ArgumentParser(description="Run the Pylone web server.")
parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run the HTTP server on (default: 8000)")
parser.add_argument("-w", "--ws-port", type=int, default=8001, help="Port to run the WebSocket server on (default: 8001)")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()

# Setup logging
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level)

# Handle CTRL+C to shutdown gracefully
def shutdown_server(signal, frame):
    print("\nCaptain, we are shutting down the server gracefully... 🖖")
    app.shutdown()  # Shutdown the WebSocket server
    sys.exit(0)

# Bind SIGINT (CTRL+C) to the shutdown function
signal.signal(signal.SIGINT, shutdown_server)

# Start the servers
if __name__ == '__main__':
    app.run(http_host="127.0.0.1", http_port=args.port, ws_host="127.0.0.1", ws_port=args.ws_port)