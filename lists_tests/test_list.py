from http import HTTPStatus
import requests
from conftest import URL


class Testists:

    def test_create_list_on_board(self, prepare_list_on_board):
        assert prepare_list_on_board.status_code == HTTPStatus.OK

    def test_rename_list(self, prepare_list_on_board, credentials):
        list_id = prepare_list_on_board.json()["id"]
        list_url = URL + "lists/" + list_id
        new_name = "New name"
        querystring = {"name": new_name}
        querystring.update(credentials)

        assert (requests.put(list_url, params=querystring)).json()["name"] == new_name

    def test_archive_non_empty_list(self, create_card_and_list_on_board, credentials, logger):
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
