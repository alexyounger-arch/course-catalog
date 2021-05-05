from tests.client_request import ClientRequest as cr


def test_add_course(client):
    """test /add-course endpoint"""
    rv = cr.add_course(client, 'math', '2021-11-03', '2021-11-04', 12)
    expected = {"Message": 'success'}
    assert rv.get_json() == expected, 'wrong response with valid fields'

    rv = cr.get_course(client, 1)
    expected = {"course": {
        "id": 1,
        "course": "math",
        "start_date": "2021-11-03",
        "end_date": "2021-11-04",
        "num_of_lecture": 12
    }}
    assert rv.get_json() == expected, 'course not added'

    rv = cr.add_course(client, 'math', '2021-02-02', '2021-01-01', 12)
    expected = {'Error': 'start_date greater then end_date'}
    assert rv.get_json() == expected, 'accepted dates, where start data greater then end date'

    rv = cr.add_course(client, 'math', '2021-11-89', '2021-11-04', 12)
    expected = {'Error': 'invalid dates'}
    assert rv.get_json() == expected, 'accepted invalid dates'


def test_get_courses(client):
    """test /get-courses endpoint"""
    rv = cr.get_courses(client)
    response = rv.get_json()
    expected = {'courses': []}
    assert response == expected

    cr.add_course(client, 'math', '2021-11-03', '2021-11-04', 12)
    cr.add_course(client, 'physics', '2021-03-15', '2021-03-30', 6)
    cr.add_course(client, 'python', '2021-06-01', '2021-07-01', 4)
    rv = cr.get_courses(client)
    response = rv.get_json()
    expected = {'courses': ['math', 'physics', 'python']}
    assert response == expected


def test_get_course(client):
    """test /get-course endpoint"""
    cr.add_course(client, 'math', '2021-11-03', '2021-11-04', 12)
    cr.add_course(client, 'physics', '2021-03-15', '2021-03-30', 6)
    rv = cr.get_course(client, 2)
    expected = {"course": {
        "id": 2,
        "course": "physics",
        "start_date": '2021-03-15',
        "end_date": '2021-03-30',
        "num_of_lecture": 6
    }}
    assert rv.get_json() == expected, 'received incorrect course data'

    rv = cr.get_course(client, 9)
    expected = {'course': []}
    assert rv.get_json() == expected, 'request with invalid id return not empty list'


def test_filtered_courses(client):
    """test /get-filtered-courses endpoint"""
    cr.add_course(client, 'math', '2021-01-10', '2021-02-10', 12)
    cr.add_course(client, 'math', '2021-03-10', '2021-04-10', 7)
    cr.add_course(client, 'physics', '2021-05-15', '2021-05-30', 6)
    cr.add_course(client, 'python', '2021-06-01', '2021-07-01', 4)
    rv = cr.get_filtered_courses(client, 'math', '2021-01-01', '2021-12-01')
    expected = {'courses': [{
        "id": 1,
        "course": "math",
        "start_date": "2021-01-10",
        "end_date": "2021-02-10",
        "num_of_lecture": 12
    }, {
        "id": 2,
        "course": "math",
        "start_date": "2021-03-10",
        "end_date": "2021-04-10",
        "num_of_lecture": 7
    }]}
    assert rv.get_json() == expected, 'simple request'

    rv = cr.get_filtered_courses(client, 'math', '2021-01-01', '2021-03-15')
    expected = {'courses': [{
        "id": 1,
        "course": "math",
        "start_date": "2021-01-10",
        "end_date": "2021-02-10",
        "num_of_lecture": 12
    }]}
    assert rv.get_json() == expected, 'request with dates that do not include all courses of the given title'

    rv = cr.get_filtered_courses(client, 'math', '2020-01-01', '2020-12-01')
    expected = {'courses': []}
    assert rv.get_json() == expected, 'request with dates that arnt in the db'

    rv = cr.get_filtered_courses(client, 'C++', '2021-01-01', '2021-12-01')
    expected = {'courses': []}
    assert rv.get_json() == expected, 'request with course name that arnt in the db'

    rv = cr.get_filtered_courses(client, 'p%', '2021-01-01', '2021-12-01')
    expected = {'courses': [{
        "id": 3,
        "course": "physics",
        "start_date": "2021-05-15",
        "end_date": "2021-05-30",
        "num_of_lecture": 6
    }, {
        "id": 4,
        "course": "python",
        "start_date": "2021-06-01",
        "end_date": "2021-07-01",
        "num_of_lecture": 4
    }]}
    assert rv.get_json() == expected, 'request with template in course name'

    rv = cr.get_filtered_courses(client, 'math', '2021-01-99', '2021-12-01')
    expected = {'Error': 'invalid dates'}
    assert rv.get_json() == expected, 'accepted invalid dates'

    rv = cr.get_filtered_courses(client, 'math', '2021-12-01', '2021-01-01')
    expected = {'Error': 'start_date greater then end_date'}
    assert rv.get_json() == expected, 'accepted dates, where start data greater then end date'


def test_set_attribute(client):
    """test /set-attribute endpoint"""
    cr.add_course(client, 'math', '2021-01-10', '2021-02-10', 12)
    cr.set_attribute(client, 1, 'course', 'physics')
    rv = cr.get_course(client, 1)
    expected = {"course": {
        "id": 1,
        "course": "physics",
        "start_date": "2021-01-10",
        "end_date": "2021-02-10",
        "num_of_lecture": 12
    }}
    assert rv.get_json() == expected, "the 'course' attribute has not changed"

    cr.set_attribute(client, 1, 'num_of_lecture', 0)
    rv = cr.get_course(client, 1)
    expected = {"course": {
        "id": 1,
        "course": "physics",
        "start_date": "2021-01-10",
        "end_date": "2021-02-10",
        "num_of_lecture": 0
    }}
    assert rv.get_json() == expected, "the 'num_of_lecture' attribute has not changed"

    rv = cr.set_attribute(client, 1, 'start_date', "2021-01-15")
    expected = {'Message': 'success'}
    assert rv.get_json() == expected, "the 'start_date' attribute has not changed"

    rv = cr.set_attribute(client, 1, 'start_date', "2021-03-10")
    expected = {'Error': 'start_date greater then end_date'}
    assert rv.get_json() == expected, "accepted start_date greater then end_date"

    rv = cr.set_attribute(client, 1, 'end_date', "2021-01-01")
    expected = {'Error': 'end_date less then end_date'}
    assert rv.get_json() == expected, "accepted end_date less then end_date"


def test_delete_course(client):
    """test /delete-course endpoint"""
    cr.add_course(client, 'math', '2021-01-10', '2021-02-10', 12)
    rv = cr.delete_course(client, 1)
    expected = {'Message': 'success'}
    assert rv.get_json() == expected, 'course not deleted'

    rv = cr.delete_course(client, 1)
    expected = {'Message': 'course with this id does not exist'}
    assert rv.get_json() == expected, 'request with id that does not exist'
