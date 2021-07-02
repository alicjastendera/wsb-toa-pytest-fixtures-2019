from conftest import URL
import requests
from http import HTTPStatus


class TestChecklist:

    def test_create_checklist_on_board(self, credentials, create_empty_board, logger):
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

    def test_update_checklist_on_card(self):
        pass

    def test_delete_checklist_on_card(self):
        pass
