from http import HTTPStatus


class TestParams:

    def test_create_board_with_bad_credentials(self, create_board_bad):
        assert create_board_bad.status_code != HTTPStatus.OK

    def test_create_board_with_good_credentials(self, create_board_good):
        assert create_board_good.status_code == HTTPStatus.OK
