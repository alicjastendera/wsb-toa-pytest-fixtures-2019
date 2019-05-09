from http import HTTPStatus


class Tests:

    def test_create_list(self, logger, create_list):
        assert create_list.status_code == HTTPStatus.OK

    def test_aviation_weather(self, logger, get_aviation_weather):
        assert get_aviation_weather[0].status_code == HTTPStatus.OK
