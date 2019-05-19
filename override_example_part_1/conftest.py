import pytest
import requests

URL = "https://api.trello.com/1/"


@pytest.fixture()
def create_empty_board(credentials, logger):
    """Creates empty board"""
    logger.info("Creating board with overriden fixture")
    boards_url = URL + "boards"
    querystring = {"name": "Overriden fixture with different params", "defaultLabels": "true", "defaultLists": "true",
                   "keepFromSource": "none", "prefs_permissionLevel": "private", "prefs_voting": "disabled",
                   "prefs_comments": "members", "prefs_invitations": "admins", "prefs_selfJoin": "true",
                   "prefs_background": "orange", "prefs_cardAging": "regular"}

    querystring.update(credentials)
    response = requests.post(boards_url, params=querystring)

    yield response
    board_id = response.json()["id"]
    requests.delete(boards_url + "/" + board_id, params=credentials)
