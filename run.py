import sys
import signal
import logging
from wsgiref.simple_server import make_server
from demo.app import app


# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Fancy Open-Source Banner
BANNER = r"""
██████╗ ██╗   ██╗██╗       ██████╗ ███╗   ██╗███████╗
██╔══██╗██║   ██║██║     ██╔═══██╗ ████╗  ██║██╔════╝
██████╔╝██║   ██║██║     ██║   ██║ ██╔██╗ ██║█████╗  
██╔═══╝ ██║   ██║██║     ██║   ██║ ██║╚██╗██║██╔══╝  
██║     ╚██████  ╔╝███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝      ╚══██═══╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
Pylone Framework v1.0 (c) 2025 Agile Creative Labs Inc
MIT License | Open Source & Free | Built with 🖖 by Starfleet Engineers
"""

print(BANNER)

# Handle CTRL+C to shutdown gracefully
def shutdown_server(signal, frame):
    print("\nCaptain, we are shutting down the server gracefully... 🖖")
    sys.exit(0)

# Bind SIGINT (CTRL+C) to the shutdown function
signal.signal(signal.SIGINT, shutdown_server)

# Start the WSGI server
server = make_server("localhost", 8000, app)
print("🚀 Serving on http://localhost:8000. Press CTRL+C to stop.")

server.serve_forever()
