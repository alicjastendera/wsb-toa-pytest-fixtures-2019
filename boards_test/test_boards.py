from helper import get_users_boards
from http import HTTPStatus
import pytest
import requests
from conftest import URL


class TestBoards:

    def test_create_3_empty_boards(self, credentials, create_board_factory):
        """Try to create 3 boards"""
        create_board_factory("First board")
        create_board_factory("Second board")
        create_board_factory("Third board")

        response = get_users_boards(credentials)
        open_boards = [board["name"] for board in response.json() if board["closed"] is False]

        assert len(open_boards) == 3

    @pytest.mark.parametrize("create_empty_board_with_bcg_color", ["green", "blue", "orange"], indirect=True)
    def test_create_board_with_given_background(self, create_empty_board_with_bcg_color):
        result, color = create_empty_board_with_bcg_color
        assert result.status_code == HTTPStatus.OK
        assert result.json()["prefs"]["background"] == color

    def test_rename_board(self, create_board_factory, credentials):
        board_id = create_board_factory("Name to be changed")
        new_name = "New name"

        board_url = URL + "boards/" + board_id
        querystring = {"name": new_name}
        querystring.update(credentials)
        result = requests.put(board_url, params=querystring)
        assert result.status_code == HTTPStatus.OK

        result = get_users_boards(credentials)
        boards = [board["name"] for board in result.json()]
        assert len(boards) == 1
        assert boards[0] == new_name
