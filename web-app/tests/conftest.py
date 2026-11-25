# pylint: disable=redefined-outer-name

import importlib
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def database():
    """Provide a mock database with an empty query result."""
    mock_database = MagicMock()
    mock_database.predictions.find.return_value.sort.return_value.limit.return_value = []
    return mock_database


@pytest.fixture
def app(monkeypatch, database):
    """Provide the Flask app without connecting to a real database."""
    monkeypatch.setenv(
        "MONGO_URI",
        "mongodb://mongodb:27017/project_db",
    )

    mock_client = MagicMock()
    monkeypatch.setattr("pymongo.MongoClient", mock_client)

    web_module = importlib.import_module("app")
    monkeypatch.setattr(web_module, "database", database)
    monkeypatch.setitem(web_module.app.config, "TESTING", True)

    return web_module.app