import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, db

import config


@pytest.fixture
def client():
    app.config.from_object(config.TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_load_data(client):
    data = {"file": (open("tests/test_data.csv", "rb"), "test_data.csv")}
    response = client.post("/load-data", content_type="multipart/form-data", data=data)
    assert response.status_code == 200
    assert b"Data imported successfully" in response.data


def test_export_data(client):
    data = {"file": (open("tests/test_data.csv", "rb"), "test_data.csv")}
    client.post("/load-data", content_type="multipart/form-data", data=data)

    response = client.get("/export-data?format=csv")
    assert response.status_code == 200
    assert "attachment" in response.headers["Content-Disposition"]
    assert "exported_data.csv" in response.headers["Content-Disposition"]
