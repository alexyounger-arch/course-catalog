# How to setup the project

1. git clone https://github.com/alexyounger-arch/course-catalog.git
2. cd course-catalog
3. python3 -m venv .venv
4. linux - source .venv/bin/activate, windows - .venv\scripts\activate
5. pip install -r requirements.txt
6. create a .env file and write DEBUG=True FLASK_ENV=development FLASK_APP=app.py

# Run application

1. flask init-db
2. flask run
3. flask reset-table (for reset database)

# Run tests

- pytest -v
