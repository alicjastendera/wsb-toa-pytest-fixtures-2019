from helper import get_users_boards
from http import HTTPStatus


class TestBoards:

    def test_create_3_empty_boards(self, credentials, create_board_factory):
        """Try to create 3 boards"""
        create_board_factory("First board")
        create_board_factory("Second board")
        create_board_factory("Third board")

        response = get_users_boards(credentials)
        open_boards = [board["name"] for board in response.json() if board["closed"] is False]

        assert len(open_boards) == 3

    def test_create_board_with_green_background(self, logger, create_empty_board_with_color_factory):
        result = create_empty_board_with_color_factory("green")
        assert result.status_code == HTTPStatus.OK
        assert result.json()["prefs"]["background"] == "green"

    def test_create_board_with_orange_background(self, logger, create_empty_board_with_color_factory):
        result = create_empty_board_with_color_factory("orange")
        assert result.status_code == HTTPStatus.OK
        assert result.json()["prefs"]["background"] == "orange"
