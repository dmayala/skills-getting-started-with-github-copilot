import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a shallow copy of initial activities so tests can mutate safely
    original = {k: {**v, "participants": list(v.get("participants", []))} for k, v in activities.items()}
    yield
    # restore
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)
