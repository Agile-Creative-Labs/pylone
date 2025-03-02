# demo/app.py
# Description: This script initializes and configures the Pylone web application folder named 'demo'
#              including setting up routes and applying middleware.
# Author: alex@agilecreativelabs.ca
# Date: Thu Feb 27, 2025
# Copyright: Copyright (c) 2025 Agile Creative Labs Inc
#              All rights reserved.
#
# Licensed under the [License Name, e.g., MIT License] (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    [License URL or reference]
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from whitenoise import WhiteNoise
from pylone.app import App
from demo.routes import router
from demo.middlewares.logging_middleware import LoggingMiddleware
from demo.middlewares.auth_middleware import AuthMiddleware
from demo.middlewares.staticfile_middleware import StaticFileMiddleware
from demo.settings import config  # Import the config object
import logging


# Determine the path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')
logging.info(f"Static directory: {static_dir}")  # Add this line

# Create the base app
app = App(router)

# Setup the app (call setup before wrapping with middlewares)
app.setup(router)

# Wrap the app with middlewares
app = LoggingMiddleware(app)  
app = StaticFileMiddleware(app, static_dir=static_dir)  
app = AuthMiddleware(app)  
