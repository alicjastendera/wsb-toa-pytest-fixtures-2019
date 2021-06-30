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

    def test_close_board(self, create_empty_board, credentials):
        board_id = create_empty_board.json()["id"]
        board_url = URL + "boards/" + board_id

        querystring = {"closed": "true"}
        querystring.update(credentials)
        result = requests.put(board_url, params=querystring)

        assert result.status_code == HTTPStatus.OK
        assert result.json()["closed"] is True

    def test_delete_empty_board(self, create_empty_board, credentials):
        board_id = create_empty_board.json()["id"]
        board_url = URL + "boards/" + board_id

        querystring = credentials
        result = requests.delete(board_url, params=querystring)

        assert result.status_code == HTTPStatus.OK
        assert get_users_boards(credentials).json() == []

    def test_delete_non_empty_board(self, create_empty_board, create_list_factory, credentials):
        board_id = create_empty_board.json()["id"]
        board_url = URL + "boards/" + board_id
        querystring = credentials

        assert (create_list_factory(board_id, "Test List")).status_code == HTTPStatus.OK
        assert (requests.delete(board_url, params=querystring)).status_code == HTTPStatus.OK
        assert get_users_boards(credentials).json() == []

    def test_change_boards_bcg(self, credentials, create_empty_board):
        board_id = create_empty_board.json()["id"]
        board_url = URL + "boards/" + board_id

        assert create_empty_board.json()["prefs"]["background"] == "blue"
        querystring = {"prefs/background": "pink"}
        querystring.update(credentials)

        response = requests.put(board_url, params=querystring)
        assert response.json()["prefs"]["background"] == "pink"

    def test_add_star_to_board(self, create_empty_board, credentials):
        board_id = create_empty_board.json()["id"]
        member_url = URL + "members/me/boardStars"
        board_url = URL + "boards/" + board_id + "/boardStars"

        querystring = {'idBoard': board_id, 'pos': 'top'}
        querystring.update(credentials)

        assert (requests.post(member_url, params=querystring)).status_code == HTTPStatus.OK
        assert board_id == (requests.get(board_url, params=querystring).json())[0]["idBoard"]

    @pytest.mark.parametrize('desc_len', [40, 14203, 14204, 16384])
    def test_add_description_to_board(self, create_empty_board, credentials, desc_len):
        from random import choice
        from string import ascii_lowercase
        board_id = create_empty_board.json()["id"]
        board_url = URL + "boards/" + board_id
        test_description = ''.join([choice(ascii_lowercase) for _ in range(desc_len)])

        querystring = {"desc": test_description}
        querystring.update(credentials)
        assert (requests.put(board_url, params=querystring)).status_code == HTTPStatus.OK
        assert len((requests.get(board_url, params=querystring)).json()["desc"]) == desc_len
