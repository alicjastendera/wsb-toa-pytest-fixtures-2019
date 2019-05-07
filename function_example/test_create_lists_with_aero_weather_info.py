from http import HTTPStatus


class Tests:

    def test_create_lists(self, logger, create_lists):
        assert create_lists.status_code == HTTPStatus.OK

    def test_aviation_weather(self, logger, aviation_weather):
        assert aviation_weather[0].status_code == HTTPStatus.OK
