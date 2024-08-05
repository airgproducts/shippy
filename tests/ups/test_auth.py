from shippy import UPSClient
from shippy.ups.schemas import CreateTokenResponse


def test_generate_token():
    ups_client = UPSClient()
    token_response = ups_client.create_token()
    assert token_response.status == "approved"
    assert len(token_response.access_token) > 0


def test_get_token_fetches_token(monkeypatch):
    def get_bearer_token_monkeypatch():
        return CreateTokenResponse(
            token_type="foo",
            client_id="foo",
            status="foo",
            access_token="my_token",
            expires_in="1000",
            issued_at="1000",
        )

    ups_client = UPSClient()
    assert ups_client.bearer_token is None
    monkeypatch.setattr(ups_client, "get_bearer_token", get_bearer_token_monkeypatch)
    token = ups_client.get_bearer_token()
    assert token.access_token == "my_token"


def test_auth_gets_bearer_token(monkeypatch):
    def get_bearer_token_monkeypatch():
        return CreateTokenResponse(
            token_type="foo",
            client_id="foo",
            status="foo",
            access_token="my_token",
            expires_in="1000",
            issued_at="1000",
        )

    ups_client = UPSClient()
    monkeypatch.setattr(ups_client, "get_bearer_token", get_bearer_token_monkeypatch)
    assert ups_client.headers["Authorization"] == f"Bearer my_token"
