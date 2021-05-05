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

# API description

1. Adds the course to database.  
   *Path:* /add-course  
  *Allowed methods:* POST  
  *Required fields:*  
    - **course (str)**: the name of course;
    - **start_date (str)**: the start date of the course in YYYY-MM-DD format;
    - **end_date (str)**: the end date of the course in YYYY-MM-DD format;
    - **num_of_lecture (int)**: the number of lectures.  
  *Response (dict)*: completion status message.
2. Returns the course by ID.  
  *Path:* /get-course  
  *Allowed method:* GET  
   *Required fields:*  
    - **id (int)**: the id of course;  
  *Response (dict)*: the course with its ID.
3. Returns all courses from the database.   
  *Path:* /get-courses  
  *Allowed method:* GET  
  *Response (dict)*: all courses from database.
4. Delete the course by ID.    
  *Path:* /delete-course  
  *Allowed method:* DELETE    
      *Required fields:*  
    - **id (int)**: the id of course;  
  *Response*: completion status message.
5. Update the specified course field by ID  
  *Path:* /set-attribute  
  *Allowed method:* PUT  
  *Required fields:*  
    - **attribute (str)**: the name of the attribute course;
    - **value (str)**: new value for specified attribute;
    - **id (int)**: the id of course;  
  *Response (dict)*: completion status message.
6. Search all courses that match the specified name and are in the specified date range.  
  *Path:* /get-filtered-courses  
  *Allowed methods:* GET  
  *Required fields:*  
    - **course (str)**: the name of course;
    - **start_date (str)**: the start date of the course in YYYY-MM-DD format;
    - **end_date (str)**: the end date of the course in YYYY-MM-DD format;   
  *Response (dict)*: courses that match the search criteria.