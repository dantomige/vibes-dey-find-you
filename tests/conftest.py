import pytest
import json
from pathlib import Path

@pytest.fixture
def load_fixture():
    def _load(name):
        path = Path(__file__).parent / "fixtures" / name
        with open(path) as f:
            return json.load(f)
    return _load