"""Tests for the prediction dashboard."""

from pymongo.errors import ServerSelectionTimeoutError


def test_home_displays_records(client, database):
    """Display prediction values returned by the database."""
    records = [
        {
            "label": "cup",
            "confidence": 0.94,
            "captured_at": "2026-11-24T14:00:00Z",
            "source": "mock",
        }
    ]
    database.predictions.find.return_value.sort.return_value.limit.return_value = records

    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "cup" in page
    assert "94.0%" in page
    assert "2026-11-24T14:00:00Z" in page
    assert "mock" in page


def test_home_displays_empty_state(client):
    """Display a helpful message when no records exist."""
    response = client.get("/")

    assert response.status_code == 200
    assert "No records found" in response.get_data(as_text=True)


def test_home_handles_database_failure(client, database):
    """Return a service error when the database is unavailable."""
    database.predictions.find.side_effect = ServerSelectionTimeoutError(
        "Database unavailable"
    )

    response = client.get("/")

    assert response.status_code == 503
    assert "Unable to read the database" in response.get_data(as_text=True)


def test_home_escapes_record_content(client, database):
    """Escape record content instead of rendering it as HTML."""
    records = [
        {
            "label": "<script>alert(1)</script>",
            "confidence": 0.9,
            "captured_at": "2026-11-24T14:00:00Z",
            "source": "mock",
        }
    ]
    database.predictions.find.return_value.sort.return_value.limit.return_value = records

    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page
