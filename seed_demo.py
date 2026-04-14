"""
seed_demo.py
Run once after deployment to create the demo user and pre-load sample data.
Usage: flask seed-demo  (or: python seed_demo.py)
"""

from datetime import datetime, date, timedelta
import json
import random
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import (
    User, Course, Project, Repository, Concept,
    Library, API, Tool, Resource, Event,
    project_concept, library_concept, api_concept,
    tool_concept, resource_concept
)


def generate_commit_history(repo_name, avg_per_week=3, weeks=52):
    """
    Generate realistic-looking commit history JSON for a repository.
    Mimics the format stored by the GitHub API chain.
    Returns list of commit objects matching GitHub API response format.
    """
    commits = []
    today = datetime.now()

    for week in range(weeks):
        # Vary activity — some weeks busier, some quiet
        week_commits = max(0, int(random.gauss(avg_per_week, 1.5)))
        for _ in range(week_commits):
            # Random day within the week
            days_ago = (week * 7) + random.randint(0, 6)
            commit_date = today - timedelta(days=days_ago)

            commits.append({
                "commit": {
                    "author": {
                        "date": commit_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "name": "Alex Chen"
                    },
                    "message": random.choice([
                        "Add feature implementation",
                        "Fix bug in route handler",
                        "Update models",
                        "Refactor for clarity",
                        "Add error handling",
                        "Update dependencies",
                        "Initial commit",
                        "Add form validation",
                        "Clean up templates",
                        "Add docstrings"
                    ])
                },
                "sha": f"{''.join(random.choices('abcdef0123456789', k=40))}"
            })

    return commits


def seed():
    with app.app_context():
        # ── GUARD: don't re-seed if demo user exists ──────────────────────
        existing = db.session.execute(
            db.select(User).where(User.email == "demo@myrise.dev")
        ).scalar()
        if existing:
            print("Demo user already exists. Skipping seed.")
            return

        print("Seeding demo data...")

        # ── 1. DEMO USER ───────────────────────────────────────────────────
        user = User(
            email="demo@myrise.dev",
            name="demo",
            display_name="Alex Chen",
            password=generate_password_hash("myrise-demo",
                                            method='pbkdf2:sha256',
                                            salt_length=8),
            last_called_repos=datetime.now(),
            latest_etag_repos="demo-etag-placeholder"
        )
        db.session.add(user)
        db.session.flush()  # get user.id before committing

        # ── 2. REPOSITORIES (with seeded commit history) ───────────────────
        repo_configs = [
            ("python-100-days",      4,  52),   # busy repo, full year
            ("flask-projects",       3,  40),
            ("data-analysis",        2,  30),
            ("django-portfolio",     5,  20),   # recent, very active
            ("small-projects",       2,  45),
            ("api-practice",         1,  25),
            ("algorithms-practice",  1,  35),
        ]

        repos = {}
        for name, avg_commits, weeks in repo_configs:
            commit_data = generate_commit_history(name, avg_commits, weeks)
            repo = Repository(
                name=name,
                commits_data=commit_data,
                commits_etag=f"demo-etag-{name}",
                created_at=datetime.now() - timedelta(weeks=weeks),
                updated_at=datetime.now() - timedelta(days=random.randint(1, 14)),
                pushed_at=datetime.now() - timedelta(days=random.randint(1, 7)),
                latest_sha=f"{''.join(random.choices('abcdef0123456789', k=40))}",
                user_id=user.id
            )
            db.session.add(repo)
            db.session.flush()
            repos[name] = repo

        # ── 3. CONCEPTS ────────────────────────────────────────────────────
        concept_data = [
            # Libraries
            ("Flask",           "library"),
            ("SQLAlchemy",      "library"),
            ("Pandas",          "library"),
            ("NumPy",           "library"),
            ("Requests",        "library"),
            ("Flask-Login",     "library"),
            ("Flask-WTF",       "library"),
            ("WTForms",         "library"),
            ("Werkzeug",        "library"),
            ("Jinja2",          "library"),
            ("Matplotlib",      "library"),
            ("Plotly",          "library"),
            ("BeautifulSoup4",  "library"),
            ("Pytest",          "library"),
            ("Flask-SQLAlchemy","library"),
            # APIs
            ("GitHub REST API",     "api"),
            ("Open Notify API",     "api"),
            ("OpenWeather API",     "api"),
            ("REST Countries API",  "api"),
            ("NewsAPI",             "api"),
            # Topics
            ("Authentication",      "topic"),
            ("Password Hashing",    "topic"),
            ("Session Management",  "topic"),
            ("CRUD Operations",     "topic"),
            ("Database Relationships", "topic"),
            ("Many-to-Many",        "topic"),
            ("Foreign Keys",        "topic"),
            ("ORM",                 "topic"),
            ("API Integration",     "topic"),
            ("Error Handling",      "topic"),
            ("ETag Caching",        "topic"),
            ("Async Operations",    "topic"),
            ("Threading",           "topic"),
            ("Data Visualization",  "topic"),
            ("CSV Import",          "topic"),
            ("Form Validation",     "topic"),
            ("File Upload",         "topic"),
            ("Pagination",          "topic"),
            ("Responsive Design",   "topic"),
            ("Environment Variables","topic"),
            # Functions/Patterns
            ("generate_password_hash",  "function"),
            ("@login_required",         "function"),
            ("db.session.execute",      "function"),
            ("mapped_column",           "function"),
            ("pd.read_sql",             "function"),
            ("requests.get",            "function"),
            ("url_for",                 "function"),
            ("flash()",                 "function"),
            # Tools
            ("VS Code",         "tool"),
            ("Git",             "tool"),
            ("Postman",         "tool"),
            ("Railway",         "tool"),
            ("TablePlus",       "tool"),
            ("PyCharm",         "tool"),
            ("Jupyter Notebook","tool"),
        ]

        concepts = {}
        for term, category in concept_data:
            c = Concept(
                concept_term=term,
                category=category,
                description=f"Used in multiple projects — see linked items.",
                date_added=date.today() - timedelta(days=random.randint(10, 400))
            )
            db.session.add(c)
            db.session.flush()
            concepts[term] = c

        # ── 4. COURSES ─────────────────────────────────────────────────────
        courses_data = [
            # (name, platform, instructor, hours, has_cert, status, start, complete)
            ("100 Days of Code: Python Bootcamp",
             "Udemy", "Dr. Angela Yu", 60, True, "complete",
             date(2023, 6, 1), date(2023, 11, 15)),

            ("The Flask Mega-Tutorial",
             "Self-Paced (miguelgrinberg.com)", "Miguel Grinberg", 20, False, "complete",
             date(2023, 9, 1), date(2023, 10, 20)),

            ("SQL and Databases Bootcamp",
             "Udemy", "Jose Portilla", 14, True, "complete",
             date(2023, 10, 1), date(2023, 11, 30)),

            ("Python for Data Science and ML",
             "Udemy", "Jose Portilla", 25, True, "complete",
             date(2023, 12, 1), date(2024, 2, 10)),

            ("CS50P: Python",
             "edX (Harvard)", "David Malan", 15, True, "complete",
             date(2024, 1, 15), date(2024, 3, 1)),

            ("Django for Beginners",
             "Self-Paced (djangoforbeginners.com)", "William Vincent", 12, False, "complete",
             date(2024, 2, 1), date(2024, 3, 15)),

            ("REST APIs with Flask and Python",
             "Udemy", "Jose Salvatierra", 17, True, "complete",
             date(2024, 3, 1), date(2024, 4, 20)),

            ("Data Visualization with Python",
             "Coursera", "IBM Skills Network", 10, True, "complete",
             date(2024, 4, 1), date(2024, 5, 10)),

            ("freeCodeCamp: Data Analysis with Python",
             "freeCodeCamp", "freeCodeCamp", 8, True, "complete",
             date(2024, 5, 1), date(2024, 6, 15)),

            ("Automate the Boring Stuff with Python",
             "Self-Paced (automatetheboringstuff.com)", "Al Sweigart", 12, False, "complete",
             date(2024, 6, 1), date(2024, 7, 30)),

            ("Python Testing with Pytest",
             "Self-Paced", "Brian Okken", 8, False, "in-progress",
             date(2024, 10, 1), None),

            ("FastAPI Modern Python Web Development",
             "Udemy", "Bill Lubanovic", 12, False, "in-progress",
             date(2025, 1, 1), None),

            ("PostgreSQL Bootcamp",
             "Udemy", "Adnan Waheed", 14, False, "not-started",
             None, None),

            ("Docker and Kubernetes",
             "Udemy", "Bret Fisher", 20, False, "not-started",
             None, None),
        ]

        courses = {}
        for (name, platform, instructor, hours, has_cert,
             status, start, complete) in courses_data:
            c = Course(
                name=name,
                platform=platform,
                instructor=instructor,
                content_hours=hours,
                has_cert=has_cert,
                status=status,
                start=start,
                complete=complete,
                date_added=start or date(2024, 1, 1),
                url="",
                user_id=user.id
            )
            db.session.add(c)
            db.session.flush()
            courses[name] = c

        # ── 5. PROJECTS ────────────────────────────────────────────────────
        projects_data = [
            # (name, course_key, repo_key, path, description, concept_keys)
            ("Password Manager CLI",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-019",
             "CLI password manager using Python's pyperclip and file I/O",
             ["File Upload", "Error Handling"]),

            ("Caesar Cipher",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-008",
             "Encryption tool implementing Caesar cipher with encode/decode",
             ["Error Handling"]),

            ("Blackjack Game",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-011",
             "Terminal blackjack with full game logic and score tracking",
             ["Error Handling"]),

            ("Web Scraper: Top 100 Movies",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-045",
             "BeautifulSoup scraper pulling top 100 movies from Empire Magazine",
             ["BeautifulSoup4", "Requests", "API Integration"]),

            ("Automated Birthday Emailer",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-032",
             "Reads CSV of birthdays, sends personalized emails automatically",
             ["CSV Import", "Async Operations"]),

            ("ISS Overhead Notifier",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-033",
             "Checks ISS position + sunset API; sends email if ISS is overhead at night",
             ["Open Notify API", "Requests", "API Integration", "Error Handling"]),

            ("Pomodoro Timer",
             "100 Days of Code: Python Bootcamp",
             "python-100-days", "day-028",
             "Desktop productivity timer with Tkinter UI and session tracking",
             ["Async Operations"]),

            ("Blog with Flask + SQLite",
             "The Flask Mega-Tutorial",
             "flask-projects", "/",
             "Multi-user blog app with user auth, posts, pagination, and full-text search",
             ["Flask", "SQLAlchemy", "Flask-Login", "Authentication",
              "Session Management", "Pagination", "CRUD Operations"]),

            ("URL Shortener API",
             "REST APIs with Flask and Python",
             "flask-projects", "url-shortener",
             "RESTful API for URL shortening with Flask + SQLite, deployed to Railway",
             ["Flask", "SQLAlchemy", "API Integration", "Railway",
              "CRUD Operations", "Error Handling"]),

            ("User Auth System",
             "The Flask Mega-Tutorial",
             "flask-projects", "auth-module",
             "Standalone Flask auth implementation: register, login, hashed passwords, sessions",
             ["Flask-Login", "Flask-WTF", "Authentication",
              "Password Hashing", "Session Management", "WTForms"]),

            ("Contact Book App",
             "The Flask Mega-Tutorial",
             "flask-projects", "contact-book",
             "CRUD contact manager with search and pagination",
             ["Flask", "SQLAlchemy", "CRUD Operations", "Pagination",
              "Form Validation", "WTForms"]),

            ("Sales Data Analysis",
             "Python for Data Science and ML",
             "data-analysis", "sales-analysis",
             "Pandas analysis of 12-month sales data with monthly revenue trends and top products",
             ["Pandas", "NumPy", "Matplotlib", "Data Visualization",
              "CSV Import"]),

            ("Student Grade Analyzer",
             "freeCodeCamp: Data Analysis with Python",
             "data-analysis", "grade-analyzer",
             "Statistical analysis of student grade distributions with histogram visualization",
             ["Pandas", "NumPy", "Matplotlib", "Data Visualization"]),

            ("Stock Price Dashboard",
             "Data Visualization with Python",
             "data-analysis", "stock-dashboard",
             "Interactive Plotly dashboard comparing stock performance across sectors",
             ["Pandas", "Plotly", "Data Visualization", "API Integration"]),

            ("Weather CLI Tool",
             "100 Days of Code: Python Bootcamp",
             "api-practice", "weather-cli",
             "Command-line weather tool using OpenWeather API with city search",
             ["OpenWeather API", "Requests", "API Integration",
              "Error Handling", "requests.get"]),

            ("News Aggregator",
             "REST APIs with Flask and Python",
             "api-practice", "news-api",
             "Flask app pulling top headlines from NewsAPI with category filtering",
             ["NewsAPI", "Flask", "Requests", "API Integration",
              "ETag Caching", "Error Handling"]),

            ("Country Explorer",
             "100 Days of Code: Python Bootcamp",
             "api-practice", "countries",
             "REST Countries API wrapper with search, filter by region, and data display",
             ["REST Countries API", "Requests", "API Integration"]),

            ("GitHub Repo Lister",
             "REST APIs with Flask and Python",
             "api-practice", "github-repos",
             "Fetches and displays public repos for any GitHub user with language stats",
             ["GitHub REST API", "Requests", "API Integration",
              "ETag Caching", "requests.get"]),

            ("AURA Portfolio Site",
             "Django for Beginners",
             "django-portfolio", "/",
             "HUD-themed Django portfolio: three-app architecture, custom admin, DataLog system",
             ["Flask", "SQLAlchemy", "Authentication", "CRUD Operations",
              "Database Relationships", "Many-to-Many", "ORM", "Railway"]),

            ("Binary Search Implementation",
             "CS50P: Python",
             "algorithms-practice", "binary-search",
             "Iterative and recursive binary search with complexity analysis",
             ["Error Handling"]),

            ("Sorting Algorithm Visualizer",
             "CS50P: Python",
             "algorithms-practice", "sorting",
             "Step-by-step visualizer for bubble, merge, and quicksort",
             ["Data Visualization"]),

            ("File Organizer Script",
             "Automate the Boring Stuff with Python",
             "small-projects", "file-organizer",
             "Watches a downloads folder and auto-sorts files by extension into subdirectories",
             ["Async Operations", "Error Handling", "File Upload"]),

            ("PDF Merger CLI",
             "Automate the Boring Stuff with Python",
             "small-projects", "pdf-merger",
             "CLI tool to merge, split, and reorder PDF pages using pypdf",
             ["File Upload", "Error Handling"]),

            ("CSV Data Cleaner",
             "Automate the Boring Stuff with Python",
             "small-projects", "csv-cleaner",
             "Detects and fixes common CSV issues: duplicate rows, missing values, encoding errors",
             ["Pandas", "CSV Import", "Error Handling"]),

            ("myRise Learning Platform",
             "The Flask Mega-Tutorial",
             "flask-projects", "myrise",
             "Personal learning OS: course tracker, project library, GitHub analytics, concept tagging",
             ["Flask", "SQLAlchemy", "Flask-Login", "Flask-WTF",
              "Authentication", "Many-to-Many", "CRUD Operations",
              "GitHub REST API", "ETag Caching", "Threading",
              "Async Operations", "Pandas", "CSV Import",
              "Database Relationships", "Foreign Keys", "ORM"]),
        ]

        for (name, course_key, repo_key, path,
             description, concept_keys) in projects_data:
            p = Project(
                name=name,
                description=description,
                path=path,
                start=date(2023, 6, 1) + timedelta(
                    days=random.randint(0, 500)),
                date_added=date.today() - timedelta(
                    days=random.randint(30, 500)),
                section="",
                lecture="",
                course_id=courses[course_key].id,
                repo_id=repos[repo_key].id,
                user_id=user.id
            )
            db.session.add(p)
            db.session.flush()

            # Tag with concepts
            for term in concept_keys:
                if term in concepts:
                    db.session.execute(
                        project_concept.insert().values(
                            project_id=p.id,
                            concept_id=concepts[term].id
                        )
                    )

        # ── 6. LIBRARIES ───────────────────────────────────────────────────
        libs_data = [
            ("Flask",       "Lightweight WSGI web framework for Python",
             "https://flask.palletsprojects.com",
             ["Flask", "CRUD Operations", "Authentication"]),
            ("SQLAlchemy",  "Python SQL toolkit and ORM",
             "https://docs.sqlalchemy.org",
             ["SQLAlchemy", "ORM", "Database Relationships"]),
            ("Pandas",      "Data analysis and manipulation library",
             "https://pandas.pydata.org/docs",
             ["Pandas", "Data Visualization", "CSV Import"]),
            ("NumPy",       "Numerical computing with multi-dimensional arrays",
             "https://numpy.org/doc",
             ["NumPy"]),
            ("Requests",    "Elegant HTTP library for Python",
             "https://requests.readthedocs.io",
             ["Requests", "API Integration", "requests.get"]),
            ("Flask-Login", "User session management for Flask",
             "https://flask-login.readthedocs.io",
             ["Flask-Login", "Authentication", "Session Management"]),
            ("Flask-WTF",   "Integration of Flask and WTForms with CSRF protection",
             "https://flask-wtf.readthedocs.io",
             ["Flask-WTF", "WTForms", "Form Validation"]),
            ("Werkzeug",    "WSGI utility library — password hashing, routing, debugging",
             "https://werkzeug.palletsprojects.com",
             ["Werkzeug", "Password Hashing", "Authentication"]),
            ("Plotly",      "Interactive graphing library for Python",
             "https://plotly.com/python",
             ["Plotly", "Data Visualization"]),
            ("Matplotlib",  "2D plotting library",
             "https://matplotlib.org/stable/contents.html",
             ["Matplotlib", "Data Visualization"]),
            ("BeautifulSoup4", "HTML/XML parsing library for web scraping",
             "https://www.crummy.com/software/BeautifulSoup/bs4/doc",
             ["BeautifulSoup4", "API Integration"]),
            ("python-dotenv","Reads key-value pairs from .env files",
             "https://pypi.org/project/python-dotenv",
             ["Environment Variables"]),
            ("Flask-SocketIO","Socket.IO integration for Flask apps",
             "https://flask-socketio.readthedocs.io",
             ["Async Operations", "Threading"]),
            ("Pytest",      "Testing framework for Python",
             "https://docs.pytest.org",
             ["Pytest"]),
            ("Pillow",      "Python Imaging Library fork",
             "https://pillow.readthedocs.io",
             ["File Upload"]),
            ("gunicorn",    "Python WSGI HTTP server for Unix",
             "https://docs.gunicorn.org",
             ["Railway"]),
            ("psycopg2",    "PostgreSQL adapter for Python",
             "https://www.psycopg.org/docs",
             ["SQLAlchemy", "Database Relationships"]),
            ("Jinja2",      "Template engine for Python used by Flask",
             "https://jinja.palletsprojects.com",
             ["Jinja2", "Flask"]),
        ]

        for name, desc, doc_link, concept_keys in libs_data:
            lib = Library(
                name=name,
                description=desc,
                doc_link=doc_link,
                date_added=date.today() - timedelta(days=random.randint(10, 400)),
                user_id=user.id
            )
            db.session.add(lib)
            db.session.flush()
            for term in concept_keys:
                if term in concepts:
                    db.session.execute(
                        library_concept.insert().values(
                            library_id=lib.id,
                            concept_id=concepts[term].id
                        )
                    )

        # ── 7. APIs ────────────────────────────────────────────────────────
        apis_data = [
            ("GitHub REST API",
             "Full GitHub platform API — repos, commits, events, users",
             "https://api.github.com",
             "https://docs.github.com/en/rest", True,
             ["GitHub REST API", "ETag Caching", "API Integration"]),
            ("Open Notify API",
             "Real-time ISS position and astronaut data",
             "http://api.open-notify.org",
             "http://open-notify.org/Open-Notify-API", False,
             ["Open Notify API", "API Integration", "Requests"]),
            ("OpenWeather API",
             "Current weather, forecasts, and historical data",
             "https://api.openweathermap.org",
             "https://openweathermap.org/api", True,
             ["OpenWeather API", "API Integration"]),
            ("REST Countries API",
             "Country data — population, currencies, languages, flags",
             "https://restcountries.com/v3.1",
             "https://restcountries.com", False,
             ["REST Countries API", "API Integration", "Requests"]),
            ("NewsAPI",
             "Real-time and historical news articles from 80k+ sources",
             "https://newsapi.org/v2",
             "https://newsapi.org/docs", True,
             ["NewsAPI", "API Integration", "ETag Caching"]),
            ("Sunrise-Sunset API",
             "Sunrise and sunset times for any lat/lon coordinate",
             "https://api.sunrise-sunset.org",
             "https://sunrise-sunset.org/api", False,
             ["API Integration", "Requests"]),
            ("Nutritionix API",
             "Natural language food and nutrition data",
             "https://api.nutritionix.com",
             "https://developer.nutritionix.com", True,
             ["API Integration"]),
            ("Sheety API",
             "Turn Google Sheets into a REST API",
             "https://api.sheety.co",
             "https://sheety.co/docs", True,
             ["API Integration", "CSV Import"]),
            ("PokeAPI",
             "RESTful API for Pokémon data — great for learning API patterns",
             "https://pokeapi.co/api/v2",
             "https://pokeapi.co/docs/v2", False,
             ["API Integration", "Requests"]),
            ("Twilio API",
             "SMS and voice messaging API",
             "https://api.twilio.com",
             "https://www.twilio.com/docs", True,
             ["API Integration", "Async Operations"]),
        ]

        for name, desc, url, doc_link, req_login, concept_keys in apis_data:
            api = API(
                name=name,
                description=desc,
                url=url,
                doc_link=doc_link,
                requires_login=req_login,
                date_added=date.today() - timedelta(days=random.randint(10, 400)),
                user_id=user.id
            )
            db.session.add(api)
            db.session.flush()
            for term in concept_keys:
                if term in concepts:
                    db.session.execute(
                        api_concept.insert().values(
                            api_id=api.id,
                            concept_id=concepts[term].id
                        )
                    )

        # ── 8. TOOLS ───────────────────────────────────────────────────────
        tools_data = [
            ("VS Code",         "essentials",
             "Primary code editor with Python extension pack",
             "https://code.visualstudio.com",
             "https://code.visualstudio.com/docs",
             ["VS Code"]),
            ("Git",             "essentials",
             "Version control — daily use for all projects",
             "https://git-scm.com",
             "https://git-scm.com/doc",
             ["Git"]),
            ("PyCharm",         "essentials",
             "JetBrains IDE for Python — used for larger projects",
             "https://www.jetbrains.com/pycharm",
             "https://www.jetbrains.com/pycharm/documentation",
             ["PyCharm"]),
            ("Postman",         "essentials",
             "API development and testing tool",
             "https://www.postman.com",
             "https://learning.postman.com/docs",
             ["Postman", "API Integration"]),
            ("Jupyter Notebook","data-science",
             "Interactive computing environment for data exploration",
             "https://jupyter.org",
             "https://jupyter-notebook.readthedocs.io",
             ["Jupyter Notebook", "Data Visualization", "Pandas"]),
            ("TablePlus",       "storage",
             "Database GUI for browsing SQLite and PostgreSQL",
             "https://tableplus.com",
             "https://docs.tableplus.com",
             ["TablePlus", "SQLAlchemy"]),
            ("Railway",         "hosting",
             "PaaS deployment platform — hosts Flask and Django apps",
             "https://railway.app",
             "https://docs.railway.app",
             ["Railway", "Environment Variables"]),
            ("GitHub Desktop",  "essentials",
             "GUI git client for managing branches and commits",
             "https://desktop.github.com",
             "https://docs.github.com/en/desktop",
             ["Git"]),
            ("Excalidraw",      "planning",
             "Virtual whiteboard for system diagrams and architecture sketches",
             "https://excalidraw.com",
             None,
             []),
            ("Notion",          "planning",
             "Project notes, planning docs, and learning resources",
             "https://www.notion.so",
             "https://www.notion.so/help",
             []),
            ("Streamlit",       "code-execution",
             "Framework for building data apps in Python",
             "https://streamlit.io",
             "https://docs.streamlit.io",
             ["Data Visualization"]),
            ("Black",           "essentials",
             "Opinionated Python code formatter",
             "https://github.com/psf/black",
             "https://black.readthedocs.io",
             []),
            ("Flake8",          "essentials",
             "Python linting tool for style and error checking",
             "https://flake8.pycqa.org",
             "https://flake8.pycqa.org/en/latest",
             []),
            ("Docker",          "hosting",
             "Containerization — learning for future deployment workflows",
             "https://www.docker.com",
             "https://docs.docker.com",
             ["Environment Variables"]),
            ("Heroku",          "hosting",
             "Former deployment platform — migrated to Railway",
             "https://www.heroku.com",
             "https://devcenter.heroku.com",
             ["Railway"]),
            ("ngrok",           "code-execution",
             "Expose local server to the internet for webhook testing",
             "https://ngrok.com",
             "https://ngrok.com/docs",
             ["API Integration"]),
        ]

        for name, tool_type, desc, url, doc_link, concept_keys in tools_data:
            t = Tool(
                name=name,
                type=tool_type,
                description=desc,
                url=url,
                doc_link=doc_link,
                date_added=date.today() - timedelta(days=random.randint(10, 400)),
                user_id=user.id
            )
            db.session.add(t)
            db.session.flush()
            for term in concept_keys:
                if term in concepts:
                    db.session.execute(
                        tool_concept.insert().values(
                            tool_id=t.id,
                            concept_id=concepts[term].id
                        )
                    )

        # ── COMMIT ─────────────────────────────────────────────────────────
        db.session.commit()
        print("✅ Demo data seeded successfully!")
        print(f"   Login: demo@myrise.dev / myrise-demo")
        print(f"   Users: 1")
        print(f"   Courses: {len(courses_data)}")
        print(f"   Projects: {len(projects_data)}")
        print(f"   Repositories: {len(repo_configs)}")
        print(f"   Concepts: {len(concept_data)}")
        print(f"   Libraries: {len(libs_data)}")
        print(f"   APIs: {len(apis_data)}")
        print(f"   Tools: {len(tools_data)}")


if __name__ == "__main__":
    seed()