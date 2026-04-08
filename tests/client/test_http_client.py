from unittest.mock import patch, Mock
from src.client.http_client import HTTPClient

def test_http_client_get():

    headers = {"User-Agent": "test-script"}
    url = "http://example.com"

    client = HTTPClient(headers=headers)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "ok"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        response = client.get("http://example.com")
        mock_get.assert_called_once_with(url=url, headers=headers)

        assert response.status_code == 200
        assert response.json() == {"message": "ok"}