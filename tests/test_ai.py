import json

import pytest

from aegis_agent.ai import AIClient


def test_ai_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        AIClient()


def test_patch_response_schema():
    payload = {
        "changes": [
            {
                "path": "tracking/example.py",
                "content": "VALUE = 1\n",
            }
        ]
    }

    encoded = json.dumps(payload)
    decoded = json.loads(encoded)

    assert isinstance(decoded["changes"], list)
    assert decoded["changes"][0]["path"] == "tracking/example.py"
