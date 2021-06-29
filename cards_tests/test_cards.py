from http import HTTPStatus
import requests
from conftest import URL


class TestCards:

    def test_create_and_delete_card(self, prepare_list_on_board, credentials, logger):
        list_id = prepare_list_on_board.json()["id"]
        card_url = URL + "cards/"
        querystring = {"idList": list_id}
        querystring.update(credentials)

        response = requests.post(card_url, params=querystring)  # create
        card_id = response.json()["id"]
        assert response.status_code == HTTPStatus.OK

        response = requests.delete(card_url + card_id, params=querystring)  # delete
        assert response.status_code == HTTPStatus.OK
        assert requests.get(URL + "lists/" + list_id + "/cards", params=querystring).json() == []

    def test_update_card(self):
        pass

    def test_add_checklist_to_card(self):
        pass

    def test_add_delete_sticker_to_card(self):
        pass

    def test_copy_checklist_from_card_to_card(self):
        pass
