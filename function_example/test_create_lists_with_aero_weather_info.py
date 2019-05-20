from http import HTTPStatus


class Tests:

    def test_correct_airport(self, logger, get_aviation_weather):
        aviation_weather = get_aviation_weather
        assert aviation_weather[1].startswith(aviation_weather[2])

    def test_create_list(self, logger, create_list):
        assert create_list.status_code == HTTPStatus.OK