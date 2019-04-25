import requests
import pytest
from http import HTTPStatus

from conftest import URL

board_url = URL + "boards"
querystring = {"name": "test_board", "defaultLabels": "true", "default": "true", "keepFromSource": "none",
                   "prefs_permissionLevel": "private", "prefs_voting": "disabled", "prefs_comments": "members",
                   "prefs_invitations": "members", "prefs_selfJoin": "true", "prefs_cardCovers": "true",
                   "prefs_background": "pink", "prefs_cardAging": "regular"}


@pytest.fixture()
def create_board_bad(logger, bad_credentials):
    """Try create board with bad credentials"""
    querystring.update(bad_credentials)
    response = requests.request("POST", board_url, params=querystring)
    if response.status_code == HTTPStatus.OK:
        logger.info("****** Good credentials; board created ******")
    else:
        logger.info("****** Bad credentials; can't login and create board ******")
    return response


@pytest.fixture()
def create_board_good(logger, credentials):
    """Create board with good credentials"""
    querystring.update(credentials)
    response = requests.request("POST", board_url, params=querystring)
    if response.status_code == HTTPStatus.OK:
        logger.info("****** Good credentials; board created ******")
    else:
        logger.info("****** Bad credentials; can't login and create board ******")
    yield response
    board_url_get = URL + "members/me/boards"
    response = requests.request("GET", board_url_get, params=credentials)
    board_id, = [trello_board["id"] for trello_board in response.json() if trello_board["name"] == "test_board"]

    print(board_id)

    board_url_del = URL + "/boards/"

    response = requests.request("DELETE", board_url_del + board_id, params=credentials)

    print(response.text)


def test_create_board_with_bad_credentials(create_board_bad):
    assert create_board_bad.status_code != HTTPStatus.OK


def test_create_board_with_good_credentials(create_board_good):
    assert create_board_good.status_code == HTTPStatus.OK
