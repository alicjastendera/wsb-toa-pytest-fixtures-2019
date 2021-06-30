from http import HTTPStatus
from conftest import URL
import requests


class TestLabels:

    def test_create_label_on_a_board(self, credentials, create_empty_board, create_label_on_a_board_factory):

        board_id = create_empty_board.json()["id"]
        assert create_label_on_a_board_factory("Urgent", "pink", board_id).status_code == HTTPStatus.OK
        querystring = credentials
        response = requests.get(URL + "boards/" + board_id + "/labels", params=querystring)
        label = next(item for item in response.json() if item["name"] == "Urgent")
        assert label["color"] == "pink"

    def test_delete_label_on_a_board(self, credentials, create_empty_board, create_label_on_a_board_factory, logger):
        board_id = create_empty_board.json()["id"]
        response = create_label_on_a_board_factory("Low priority", "sky", board_id)
        label_id = response.json()["id"]
        assert response.status_code == HTTPStatus.OK

        querystring = credentials
        response = requests.get(URL + "boards/" + board_id + "/labels", params=querystring)
        label = next(item for item in response.json() if item["name"] == "Low priority")
        assert label["color"] == "sky"

        requests.delete(URL + "labels/" + label_id, params=querystring)
        response = requests.get(URL + "boards/" + board_id + "/labels", params=querystring)
        label = next((item for item in response.json() if item["name"] == "Low priority"), None)
        assert label is None
