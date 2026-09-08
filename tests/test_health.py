import pytest

from conftest import assert_result


@pytest.mark.smoke
def test_root_returns_success(api):
    body = assert_result(api.get("/"), code="200", message="成功")
    assert body["data"] == "访问成功"


@pytest.mark.smoke
def test_root_response_contract(api):
    body = api.get("/").json()
    assert set(body) == {"code", "msg", "data"}
    assert all(isinstance(body[key], str) for key in ("code", "msg", "data"))


