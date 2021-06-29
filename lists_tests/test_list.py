from http import HTTPStatus
import requests
from conftest import URL


class TestLists:

    def test_create_list_on_board(self, prepare_list_on_board):
        assert prepare_list_on_board.status_code == HTTPStatus.OK

    def test_rename_list(self, prepare_list_on_board, credentials):
        list_id = prepare_list_on_board.json()["id"]
        list_url = URL + "lists/" + list_id
        new_name = "New name"
        querystring = {"name": new_name}
        querystring.update(credentials)

        assert (requests.put(list_url, params=querystring)).json()["name"] == new_name

    def test_archive_non_empty_list(self, create_card_and_list_on_board, credentials):
        list_id = create_card_and_list_on_board.json()["idList"]
        list_url = URL + "lists/" + list_id + "/closed"
        card_id = create_card_and_list_on_board.json()["id"]
        querystring = {"value": "true"}
        querystring.update(credentials)
        response = requests.put(list_url, params=querystring)

        assert response.status_code == HTTPStatus.OK
        assert (requests.get(URL + "lists/" + list_id, params=querystring)).json()["closed"] is True
        # check if card is stil active
        response = requests.get(URL+"cards/" + card_id, querystring)
        assert response.json()["closed"] is False

    def test_move_cards_between_non_empty_lists(self, prepare_list_on_board, create_list_factory,
                                                create_card_factory, credentials):
        board_id = prepare_list_on_board.json()["idBoard"]
        first_list_id = prepare_list_on_board.json()["id"]
        list_url = URL + "lists/"
        second_list_id = create_list_factory(board_id, "Second list").json()["id"]

        create_card_factory(first_list_id, "First")
        create_card_factory(first_list_id, "Second")
        create_card_factory(first_list_id, "Third")
        create_card_factory(first_list_id, "Fourth")
        create_card_factory(second_list_id, "Fifth")

        querystring = {}
        querystring.update(credentials)

        response = requests.get(list_url + first_list_id + "/cards", querystring)  # get all cards from first list
        assert len(response.json()) == 4

        querystring.update({"idBoard": board_id, "idList": second_list_id})
        requests.post(list_url + first_list_id + "/moveAllCards", querystring)  # move cards to second list

        response = requests.get(list_url + second_list_id + "/cards", querystring)  # get all cards from second list
        assert len(response.json()) == 5

    def test_move_list_between_boards(self, credentials, create_board_factory, create_list_factory):
        list_name = "List to be moved"
        first_board_id = create_board_factory("First")
        second_board_id = create_board_factory("Second")
        list_id = create_list_factory(first_board_id, list_name).json()["id"]

        querystring = {"value": second_board_id}
        querystring.update(credentials)
        requests.put(URL + "lists/" + list_id + "/idBoard", querystring)  # moving list
        assert requests.get(URL + "boards/" + second_board_id + "/lists", credentials).json()[0]["name"] == list_name
