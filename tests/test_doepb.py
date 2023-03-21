from utils import get_file_url


class TestGetFileURL:
    """Teste get_file_url."""

    def test_should_return_doe_diario_url_if_it_exists(self):
        url = "https://auniao.pb.gov.br/doe"
        substring = "diario-oficial-18-03-2023.pdf"
        expected_result = "https://auniao.pb.gov.br/servicos/doe/2023/marco/diario-oficial-18-03-2023.pdf"
        # Act
        result = get_file_url(url, substring)
        # Assert
        assert result == expected_result

    def test_should_return_none_if_url_not_found(self):
        url = "https://auniao.pb.gov.br/doe/"
        substring = "diario-oficial-19-03-2023.pdf"
        expected_result = None
        # Act
        result = get_file_url(url, substring)
        # Assert
        assert result == expected_result
