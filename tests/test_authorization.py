import pytest

from conftest import assert_result


PROTECTED_ENDPOINTS = [
    "/notice/selectAll",
    "/activity/selectAll",
    "/house/selectAll",
    "/parking/selectAll",
    "/complaint/selectAll",
    "/fixed/selectAll",
    "/user/selectPage?pageNum=1&pageSize=5",
]


@pytest.mark.auth
@pytest.mark.parametrize("path", PROTECTED_ENDPOINTS)
def test_protected_endpoints_reject_missing_token(api, path):
    body = assert_result(api.get(path), code="401", message="无效的token")
    assert body["data"] is None


@pytest.mark.auth
@pytest.mark.parametrize("token", ["not-a-jwt", "abc.def.ghi"], ids=["plain-text", "jwt-shaped"])
def test_protected_endpoint_rejects_malformed_token(api, token):
    body = assert_result(api.get("/notice/selectAll", token=token), code="401")
    assert body["msg"] in {"无效的token", "token验证失败，请重新登录"}
    assert body["data"] is None


