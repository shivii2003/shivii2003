from ingestion.client import ApiClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self):
        self.headers = {}
        self.calls = 0

    def get(self, url, params, timeout):
        self.calls += 1
        if self.calls == 1:
            return FakeResponse({"data": [{"id": 1}], "next_cursor": "page-2"})
        return FakeResponse({"data": [{"id": 2}], "next_cursor": None})


def test_cursor_pagination_reads_all_pages():
    session = FakeSession()
    client = ApiClient("https://example.test", "token", session=session)
    rows = list(client.fetch_records("orders"))
    assert rows == [{"id": 1}, {"id": 2}]
    assert session.calls == 2
