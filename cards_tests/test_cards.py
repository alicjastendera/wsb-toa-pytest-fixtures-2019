from http import HTTPStatus
import requests
from conftest import URL


class TestCards:

    def test_create_and_delete_card(self, prepare_list_on_board, credentials):
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

    def test_update_card(self, create_card_and_list_on_board, credentials):
        card_id = create_card_and_list_on_board.json()["id"]
        card_url = URL + "cards/" + card_id
        querystring = {"name": "New name", "desc": "This is a new desc of card"}
        querystring.update(credentials)

        assert (requests.put(card_url, params=querystring)).status_code == HTTPStatus.OK
        response = requests.get(card_url, params=querystring)
        assert response.json()["name"] == "New name"
        assert response.json()["desc"] == "This is a new desc of card"

    def test_change_card_cover(self, create_card_and_list_on_board, credentials):
        card_id = create_card_and_list_on_board.json()["id"]
        cover_url = URL + "cards/" + card_id + "/cover"
        querystring = {"value": {'color': 'lime', 'brightness': 'light'}}
        querystring.update(credentials)

        assert (requests.put(cover_url, json=querystring)).status_code == HTTPStatus.OK
        response = requests.get(URL + "cards/" + card_id, params=querystring)
        assert response.json()["cover"]["color"] == "lime"
        assert response.json()["cover"]["brightness"] == "light"

    def test_add_sticker_to_card(self, credentials, create_card_and_list_on_board):
        card_id = create_card_and_list_on_board.json()["id"]
        querystring = {"image": "heart", 'top': '50', 'left': '50', 'zIndex': "1"}
        querystring.update(credentials)
        stickers_URL = URL + "cards/" + card_id + "/stickers"
        assert (requests.post(stickers_URL, params=querystring)).status_code == HTTPStatus.OK

        querystring.update({"image": "thumbsup", 'top': '10', 'left': '20', 'zIndex': "2"})
        assert (requests.post(stickers_URL, params=querystring)).status_code == HTTPStatus.OK

        response = requests.get(stickers_URL, querystring)
        stickers = [item["image"] for item in response.json()]
        assert len(stickers) == 2

    def test_remove_sticker_from_card(self, credentials, create_card_and_list_on_board):
        card_id = create_card_and_list_on_board.json()["id"]
        stickers_URL = URL + "cards/" + card_id + "/stickers/"
        querystring = {"image": "clock", 'top': '70', 'left': '50', 'zIndex': "1"}
        querystring.update(credentials)
        response = requests.post(stickers_URL, params=querystring)
        assert response.status_code == HTTPStatus.OK
        sticker_id = response.json()["id"]

        requests.delete(stickers_URL + sticker_id, params=querystring)
        assert requests.get(stickers_URL, querystring).json() == []

    def test_add__and_remove_label_from_card(self, credentials, create_label_on_a_board_factory,
                                             create_card_and_list_on_board):
        card_id = create_card_and_list_on_board.json()["id"]
        board_id = create_card_and_list_on_board.json()["idBoard"]
        label_id = (create_label_on_a_board_factory("My label", "green", board_id)).json()["id"]

        querystring = {"value": label_id}
        querystring.update(credentials)
        requests.post(URL + "cards/" + card_id + "/idLabels", querystring)
        response = requests.get(URL + "cards/" + card_id, querystring)
        assert response.json()["idLabels"][0] == label_id

        requests.delete(URL + "cards/" + card_id + "/idLabels/" + label_id, params=querystring)
        response = requests.get(URL + "cards/" + card_id, querystring)
        assert len(response.json()["idLabels"]) == 0

    def test_add_and_remove_attachment_to_card(self, credentials, create_card_and_list_on_board):
        card_id = create_card_and_list_on_board.json()["id"]
        querystring = credentials
        attachment_URL = URL + "cards/" + card_id + "/attachments/"
        headers = {"Accept": "application/json"}

        import tempfile
        with tempfile.NamedTemporaryFile(mode="a+", suffix=".txt") as temp:
            temp.write('Some data')
            temp.flush()
            temp.seek(0)
            file_name = temp.name
            files = {'file': temp}
            response = requests.post(attachment_URL, files=files, params=querystring, headers=headers)
            attachment_id = response.json()["id"]
        assert response.status_code == HTTPStatus.OK

        querystring = credentials
        response = requests.get(attachment_URL, params=querystring)
        import os
        assert response.json()[0]["fileName"] == os.path.basename(file_name)

        requests.delete(attachment_URL + attachment_id, params=querystring)
        assert (requests.get(attachment_URL, params=querystring)).json() == []
