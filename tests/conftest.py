import tempfile
import os

import pytest

from app import app, init_db


@pytest.fixture
def client():
    """Test client generator
    This client fixture will be called by each individual test
    """
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
