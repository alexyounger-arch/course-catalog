import os
import sqlite3

import click
from flask import Flask, g
from flask_restful import Resource, Api, request

from utils.utils import dict_factory, valid_dates, to_date

# configuration
DATABASE = 'database.db'
SECRET_KEY = b"\xaa\xa9\xd8\x91T0d\xfd3\x9c\x19\x88\x12\xceS\x8fG'\xf4\xf0\xc0\xc0\x13"
DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db'), ))
api = Api(app)


# database initialisation
def init_db():
    """Create database and table 'catalog'"""
    with app.app_context():
        db = get_db()
        with app.open_resource('db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command("init-db")
def init_db_command():
    """Call method init_db() by command 'flask init-db'"""
    init_db()
    click.echo("Initialized the database.")


@app.cli.command("reset-table")
def reset_table():
    """Clear existing data and create new table by command 'flask reset-table'"""
    cur = get_db().cursor()
    cur.execute("DROP TABLE IF EXISTS `catalog`")
    init_db()


@app.teardown_appcontext
def close_connection(exception):
    """Commit db changes and close connection after end request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.commit()
        db.close()


def get_db():
    """Establishes a connection with database
        :return sqlite3.Connection object"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = dict_factory
    return db


class AddCourse(Resource):
    @valid_dates
    def post(self):
        """Adds the course to database"""

        query = """INSERT INTO `catalog` (course, start_date, end_date, num_of_lecture)
            VALUES (:course, :start_date, :end_date, :num_of_lecture)"""
        cur = get_db().cursor()
        cur.execute(query, request.json)
        return {"Message": 'success'}, 200


class GetCourse(Resource):
    def get(self):
        """Returns the course by ID"""

        query = "SELECT * FROM `catalog` WHERE id = :id"
        cur = get_db().cursor()
        res = cur.execute(query, request.json).fetchone()
        course = res if res is not None else []
        return {'course': course}, 200


class GetCourses(Resource):

    def get(self):
        """Returns all courses from the database"""

        query = "SELECT course FROM `catalog`"
        cur = get_db().cursor()
        res = cur.execute(query)
        courses = [row['course'] for row in res]
        return {'courses': courses}, 200


class GetFilteredCourses(Resource):

    @valid_dates
    def get(self):
        """Returns all courses that match the specified name
         and are in the specified date range"""

        # filtering by name
        query = "SELECT id, start_date, end_date FROM `catalog` WHERE course LIKE :course"
        cur = get_db().cursor()
        res = cur.execute(query, {'course': request.json.get('course')})

        # ids of courses that are included in the specified range
        filtered_ids = []
        for item in res:
            course_start = to_date(item.get('start_date'))
            course_end = to_date(item.get('end_date'))
            start_date = to_date(request.json.get('start_date'))
            end_date = to_date(request.json.get('end_date'))
            if course_start >= start_date and course_end <= end_date:
                filtered_ids.append(str(item.get('id')))

        courses = []
        if filtered_ids:
            query = f"SELECT * FROM `catalog` WHERE id IN ({','.join(filtered_ids)})"
            courses = cur.execute(query).fetchall()

        return {'courses': courses}, 200


class SetAttribute(Resource):

    def put(self):
        """Update the specified course field by ID"""

        attribute = request.json.get('attribute')
        value = request.json.get('value')
        cur = get_db().cursor()

        if attribute == 'start_date' or attribute == 'end_date':
            try:
                to_date(value)
                query = f"SELECT start_date, end_date FROM `catalog` WHERE id = :id"
                dates = cur.execute(query, {'id': request.json.get('id')}).fetchone()

                if attribute == 'start_date' and to_date(value) > to_date(dates.get('end_date')):
                    return {'Error': 'start_date greater then end_date'}, 400
                elif attribute == 'end_date' and to_date(value) < to_date(dates.get('start_date')):

                    return {'Error': 'end_date less then end_date'}, 400
            except ValueError:
                return {'Error': 'invalid date'}, 400

        query = f"UPDATE `catalog` SET {attribute} = :value WHERE id = :id"
        cur.execute(query, request.json)
        return {'Message': 'success'}, 200


class DeleteCourse(Resource):

    def delete(self):
        """Delete the course by ID"""

        cur = get_db().cursor()
        query = "SELECT * FROM `catalog` WHERE id = :id"
        res = cur.execute(query, {'id': request.json.get('id')}).fetchone()
        if res is None:
            return {'Message': 'course with this id does not exist'}

        query = "DELETE FROM `catalog` WHERE id = :id"
        cur.execute(query, request.json)
        return {'Message': 'success'}, 200


api.add_resource(AddCourse, '/add-course', methods=['POST'])
api.add_resource(GetCourse, '/get-course', methods=['GET'])
api.add_resource(GetCourses, '/get-courses', methods=['GET'])
api.add_resource(GetFilteredCourses, '/get-filtered-courses', methods=['GET'])
api.add_resource(SetAttribute, '/set-attribute', methods=['PUT'])
api.add_resource(DeleteCourse, '/delete-course', methods=['DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
