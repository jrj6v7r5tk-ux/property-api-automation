from __future__ import annotations

import os
from typing import Any

import requests


class PropertyApiClient:
    """Small HTTP client that centralizes base URL, timeout, and token handling."""

    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        self.base_url = (base_url or os.getenv("BASE_URL", "http://localhost:9090")).rstrip("/")
        self.timeout = timeout or float(os.getenv("API_TIMEOUT", "5"))
        self.session = requests.Session()

    def request(self, method: str, path: str, *, token: str | None = None, **kwargs: Any) -> requests.Response:
        headers = dict(kwargs.pop("headers", {}))
        if token is not None:
            headers["token"] = token
        return self.session.request(
            method,
            f"{self.base_url}/{path.lstrip('/')}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)


