import pytest

from conftest import assert_result


@pytest.mark.auth
@pytest.mark.parametrize(
    "payload",
    [
        {"password": "123", "role": "ADMIN"},
        {"username": "admin", "role": "ADMIN"},
        {"username": "admin", "password": "123"},
        {"username": "", "password": "123", "role": "ADMIN"},
        {"username": "admin", "password": "", "role": "ADMIN"},
        {"username": "admin", "password": "123", "role": ""},
    ],
    ids=[
        "missing-username",
        "missing-password",
        "missing-role",
        "blank-username",
        "blank-password",
        "blank-role",
    ],
)
def test_login_rejects_missing_or_blank_required_fields(api, payload):
    response = api.post("/login", json=payload)
    body = assert_result(response, code="4001", message="参数缺失")
    assert body["data"] is None


