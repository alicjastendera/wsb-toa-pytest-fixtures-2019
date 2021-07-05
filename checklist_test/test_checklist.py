from conftest import URL
import requests
from http import HTTPStatus


class TestChecklist:

    def test_create_checklist_on_board(self, credentials, create_empty_board):
        checklist_name = "Prepare report"
        board_id = create_empty_board.json()["id"]
        querystring = {"name": checklist_name}
        querystring.update(credentials)

        response = requests.post(URL + "boards/" + board_id + "/checklists", params=querystring)
        assert response.status_code == HTTPStatus.OK

    def test_create_checklist_on_card(self, credentials, create_card_and_list_on_board,
                                      create_checkitem_on_checklist_factory):
        card_id = create_card_and_list_on_board.json()["id"]
        checklist_name = "Prepare report"

        querystring = {"name": checklist_name}
        querystring.update(credentials)
        response = requests.post(URL + "cards/" + card_id + "/checklists", params=querystring)

        checklist_id = response.json()["id"]
        create_checkitem_on_checklist_factory(checklist_id, "Prepare data")
        create_checkitem_on_checklist_factory(checklist_id, "Calculate income", "top")
        create_checkitem_on_checklist_factory(checklist_id, "Send to boss")

        response = requests.get(URL + "cards/" + card_id + "/checklists", params=querystring)
        checkitems = [item["name"] for item in response.json()[0]["checkItems"]]
        assert len(checkitems) == 3

    def test_update_checklist_on_card(self, credentials, create_card_and_list_on_board,
                                      create_checkitem_on_checklist_factory):
        card_id = create_card_and_list_on_board.json()["id"]
        checklist_name = "Prepare report"

        querystring = {"name": checklist_name}
        querystring.update(credentials)
        response = requests.post(URL + "cards/" + card_id + "/checklists", params=querystring)

        checklist_id = response.json()["id"]
        checkitem_id = create_checkitem_on_checklist_factory(checklist_id, "Prepare data").json()["id"]
        checklist_URL = URL + "checklists/" + checklist_id
        checkitem_URL = checklist_URL + "/checkItems/" + checkitem_id
        assert requests.get(checkitem_URL, params=querystring).json()["state"] == "incomplete"

        querystring.update({"state": "complete", "name": "New name"})
        requests.put(URL + "cards/" + card_id + "/checkItem/" + checkitem_id, params=querystring)

        response = requests.get(checkitem_URL, params=querystring)
        assert response.json()["state"] == "complete"
        assert response.json()["name"] == "New name"

    def test_delete_checklist_on_card(self, credentials, create_card_and_list_on_board,
                                      create_checkitem_on_checklist_factory):
        card_id = create_card_and_list_on_board.json()["id"]
        checklist_name = "Prepare report"

        querystring = {"name": checklist_name}
        querystring.update(credentials)
        response = requests.post(URL + "cards/" + card_id + "/checklists", params=querystring)

        checklist_id = response.json()["id"]
        checklist_URL = URL + "checklists/" + checklist_id
        checkitem_id = create_checkitem_on_checklist_factory(checklist_id, "Prepare data").json()["id"]
        checkitem_URL = checklist_URL + "/checkItems/" + checkitem_id

        assert (requests.get(checkitem_URL, params=querystring)).status_code == HTTPStatus.OK
        requests.delete(checklist_URL, params=querystring)
        assert (requests.get(checklist_URL, params=querystring)).status_code == HTTPStatus.NOT_FOUND
        assert (requests.get(checkitem_URL, params=querystring)).status_code == HTTPStatus.NOT_FOUND

    def test_reuse_checklist(self, credentials, prepare_list_on_board, create_card_factory):
        checklist_name = "Important things"
        list_id = prepare_list_on_board.json()["id"]
        first_card_id = create_card_factory(list_id, "First card").json()["id"]
        second_card_id = create_card_factory(list_id, "Second card").json()["id"]

        querystring = {"name": checklist_name}
        querystring.update(credentials)
        response = requests.post(URL + "cards/" + first_card_id + "/checklists", params=querystring)
        checklist_id = response.json()["id"]

        querystring = {"idCard ": second_card_id, "idChecklistSource": checklist_id}
        querystring.update(credentials)
        requests.post(URL + "cards/" + second_card_id + "/checklists", params=querystring)

        response = requests.get(URL + "cards/" + second_card_id + "/checklists", params=querystring)
        assert response.json()[0]["name"] == checklist_name
