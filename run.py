import sys
import signal
import logging
import argparse
from wsgiref.simple_server import make_server
from demo.app import app



# Fancy Open-Source Banner
BANNER = r"""
██████╗ ██╗   ██╗██╗       ██████╗ ███╗   ██╗███████╗
██╔══██╗██║   ██║██║     ██╔═══██╗ ████╗  ██║██╔════╝
██████╔╝██║   ██║██║     ██║   ██║ ██╔██╗ ██║█████╗  
██╔═══╝ ██║   ██║██║     ██║   ██║ ██║╚██╗██║██╔══╝  
██║     ╚██████  ╔╝███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝      ╚══██═══╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
Pylone Framework v1.0 (c) 2025 Agile Creative Labs Inc
Apache License | Open Source & Free | Built with 🖖 by Starfleet Engineers
"""

print(BANNER)

# Command-line argument parser
parser = argparse.ArgumentParser(description="Run the Pylone web server.")
parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()

# Setup logging
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level)

# Global server variable
server = None

# Handle CTRL+C to shutdown gracefully
def shutdown_server(signal, frame):
    global server
    print("\nCaptain, we are shutting down the server gracefully... 🖖")
    #if server:
      #  server.shutdown()  # Gracefully shut down the server
    sys.exit(0)

# Bind SIGINT (CTRL+C) to the shutdown function
signal.signal(signal.SIGINT, shutdown_server)

# Start the WSGI server
if __name__ == '__main__':
    server = make_server("127.0.0.1", 8000, app)
    logging.info("🚀 Serving on http://127.0.0.1:8000. Press CTRL+C to stop.")
    server.serve_forever()