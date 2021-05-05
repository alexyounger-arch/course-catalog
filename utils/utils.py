import datetime
from flask import request


def dict_factory(cursor, row) -> dict:
    """Change format sqlite row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def to_date(date: str):
    """Convert str to datetime.date type. Format YYYY-MM-DD"""
    return (datetime.datetime.strptime(date, "%Y-%m-%d")).date()


def valid_dates(func):
    """Checks the dates that come from the request for validity"""

    def wrapper(*args, **kwargs):
        try:
            start_date = to_date(request.json.get('start_date'))
            end_date = to_date(request.json.get('end_date'))
            if start_date > end_date:
                return {'Error': 'start_date greater then end_date'}, 400

        except ValueError:
            return {'Error': 'invalid dates'}, 400

        return func(*args, **kwargs)
    return wrapper
