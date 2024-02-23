import pytest
from src.web import create_app
from src.core.database import db

@pytest.fixture(scope='module')
def context():
    app = create_app()

    ctx = app.app_context()
    ctx.push()

    yield

    ctx.pop()
