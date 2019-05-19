from http import HTTPStatus


class TestBoards:

    def test_create_board_with_blue_background(self, logger, create_empty_board):
        assert create_empty_board.status_code == HTTPStatus.OK
        assert create_empty_board.json()["prefs"]["background"] == "blue"
