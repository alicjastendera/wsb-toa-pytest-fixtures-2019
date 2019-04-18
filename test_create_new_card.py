import json
import pytest
import requests
from http import HTTPStatus

TRELLO_API_URL = "https://api.trello.com/1/"


@pytest.fixture(scope="session")
def trello_creds():
    """Gets key and token required to authenticate against API"""
    with open("credentials.json") as f:
        creds = json.load(f)
    return creds


@pytest.fixture()
def trello_list_id(credentials):
    """Gets id for pytest-list used to create test cards"""
    # get pytest-board id from all boards of credentials owner
    boards_url = TRELLO_API_URL + "/members/me/boards"
    response = requests.get(boards_url, params=credentials)
    board_id, = [trello_board["id"] for trello_board in response.json() if trello_board["name"] == "pytest-board"]
    # get pytest-list id from all lists on pytest-board
    lists_url = TRELLO_API_URL + "/boards/{}/lists".format(board_id)
    response = requests.get(lists_url, params=credentials)
    list_id, = [trello_list["id"] for trello_list in response.json() if trello_list["name"] == "pytest-list"]
    return list_id


@pytest.fixture()
def create_card_response(credentials, trello_list_id):
    """Creates card with test name and description using API"""
    cards_url = TRELLO_API_URL + "cards"
    query_params = {
        "name": "Test Name",
        "desc": "Test Description",
        "idList": trello_list_id,
    }
    query_params.update(credentials)
    response = requests.post(cards_url, params=query_params)
    yield response
    card_id = response.json()["id"]
    requests.delete(cards_url + "/" + card_id, params=trello_creds)


class TestCreateNewCard:

    def test_response_http_status_ok(self, create_card_response):
        """Tests if response status code denotes success"""
        assert create_card_response.status_code == HTTPStatus.OK

    def test_response_card_id_set(self, create_card_response):
        """Tests if response JSON has non-empty card id"""
        assert create_card_response.json()["id"]

    def test_response_card_name_correct(self, create_card_response):
        """Tests if name parameter in response JSON corresponds to request"""
        assert create_card_response.json()["name"] == "Test Name"

    def test_response_card_desc_correct(self, create_card_response):
        """Tests if desc parameter in response JSON corresponds to request"""
        assert create_card_response.json()["desc"] == "Test Description"
