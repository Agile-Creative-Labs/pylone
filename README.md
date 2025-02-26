# pylone

pylone_mvc/  
│  
├── pylone/                   # Core framework  
│   ├── __init__.py  
│   ├── app.py                # Initializes and sets up the framework  
│   ├── router.py             # Routing system  
│   ├── request.py            # Request handling  
│   ├── response.py           # Response handling  
│   ├── template.py           # Simple template engine  
│   ├── session.py            # Session management  
│   ├── database.py           # Database connection and setup  
│   ├── middleware.py         # Middleware support (optional)  
│   ├── error_handler.py      # Generic error logging  
│  
├── demo/                     # Demo application using Pylone MVC  
│   ├── __init__.py  
│   ├── app.py                # Initializes demo application, routes, and database  
│   ├── routes.py             # Defines application routes  
│   ├── database.py           # SQLite database setup & user authentication functions  
│  
│   ├── controllers/          # Controller layer  
│   │   ├── __init__.py  
│   │   ├── auth_controller.py  # Handles login & registration  
│   │   ├── dashboard_controller.py  # Handles dashboard logic  
│  
│   ├── models/               # Model layer (Optional, if needed)  
│   │   ├── __init__.py  
│   │   ├── user_model.py      # User model logic  
│  
│   ├── templates/            # View layer (HTML templates)  
│   │   ├── index.html  
│   │   ├── login.html  
│   │   ├── register.html  
│   │   ├── dashboard.html  
│  
│   ├── static/               # Static files (CSS, JS, Images)  
│   │   ├── css/  
│   │   │   ├── style.css  
│   │   ├── js/  
│   │   │   ├── main.js  
│  
├── run.py                    # Entry point to start the WSGI server  
├── requirements.txt           # Dependencies for the project  
├── README.md                  # Documentation  
