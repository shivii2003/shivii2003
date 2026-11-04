from __future__ import annotations

import logging
import time
from typing import Any
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class ApiClient:
    """Small REST client with bounded retries and cursor pagination."""

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout_seconds: int = 30,
        max_retries: int = 4,
        page_size: int = 200,
        session: requests.Session | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required")
        if max_retries < 0 or page_size < 1:
            raise ValueError("max_retries must be >= 0 and page_size must be >= 1")
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.page_size = page_size
        self.session = session or requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        })

    def _get(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(
                    url, params=params, timeout=self.timeout_seconds
                )
                if response.status_code == 429 or response.status_code >= 500:
                    response.raise_for_status()
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    raise ValueError("API response must be a JSON object")
                return payload
            except (requests.Timeout, requests.ConnectionError, requests.HTTPError):
                if attempt >= self.max_retries:
                    raise
                delay = min(2 ** attempt, 30)
                logger.warning("API request failed; retrying attempt=%s", attempt + 1)
                time.sleep(delay)
        raise RuntimeError("unreachable retry state")

    def fetch_records(self, endpoint: str, updated_since: str | None = None):
        """Yield records from {data, next_cursor} API pages."""
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {"limit": self.page_size}
            if cursor:
                params["cursor"] = cursor
            if updated_since:
                params["updated_since"] = updated_since
            payload = self._get(url, params)
            records = payload.get("data", [])
            if not isinstance(records, list):
                raise ValueError("API field 'data' must be a list")
            for record in records:
                if not isinstance(record, dict):
                    raise ValueError("API records must be JSON objects")
                yield record
            cursor = payload.get("next_cursor")
            if not cursor:
                break
