import os

from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

client = MongoClient(
    os.environ["MONGO_URI"],
    serverSelectionTimeoutMS=3000,
)
database = client.get_default_database()


@app.get("/")
def index():
    """Read the latest predictions and render the dashboard."""
    try:
        records = list(
            database.predictions.find()
            .sort("captured_at", -1)
            .limit(20)
        )
    except PyMongoError:
        app.logger.exception("Failed to query MongoDB")
        return render_template(
            "index.html",
            records=[],
            error="Unable to read the database. Check MongoDB and its configuration.",
        ), 503

    return render_template(
        "index.html",
        records=records,
        error=None,
    )