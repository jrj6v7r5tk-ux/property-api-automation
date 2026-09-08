from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from property_api.client import PropertyApiClient


@pytest.fixture(scope="session")
def api() -> PropertyApiClient:
    client = PropertyApiClient()
    try:
        response = client.get("/")
    except Exception as exc:
        pytest.exit(f"被测系统不可访问：{client.base_url} ({exc})", returncode=2)
    if response.status_code != 200:
        pytest.exit(f"被测系统健康检查失败：HTTP {response.status_code}", returncode=2)
    return client


def assert_result(response, *, code: str, message: str | None = None) -> dict:
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    body = response.json()
    assert body["code"] == code
    if message is not None:
        assert body["msg"] == message
    assert "data" in body
    return body


