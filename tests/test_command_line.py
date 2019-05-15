from chatroom import command_line

from unittest.mock import patch
import pathlib
import ssl


def test_get_ssl_context():
    ssl_path = pathlib.Path('certifications/cert_with_key.pem')

    with patch('chatroom.command_line.ssl.SSLContext') as mock_ssl:
        mock_context = mock_ssl.return_value
        command_line.get_ssl_context('server', ssl_path)
        # test get_ssl_context without argument client_cert
        mock_ssl.assert_called_once_with(ssl.PROTOCOL_TLS_SERVER)
        mock_context.load_cert_chain.assert_called_with(ssl_path)
        mock_context.load_verify_locations.assert_not_called()
