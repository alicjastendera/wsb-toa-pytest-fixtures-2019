import requests
import pytest

from http import HTTPStatus

URL = "https://api.trello.com/1/"

board_url = URL + "boards"
querystring = {"name": "TEST_BOARD", "defaultLabels": "true", "default": "true", "keepFromSource": "none",
                   "prefs_permissionLevel": "private", "prefs_voting": "disabled", "prefs_comments": "members",
                   "prefs_invitations": "members", "prefs_selfJoin": "true", "prefs_cardCovers": "true",
                   "prefs_background": "pink", "prefs_cardAging": "regular"}


@pytest.fixture(params=[{"key"}, {"token"}, {"key", "token"}])
def create_board_bad(request, logger, credentials):
    """Try to create board with bad credentials"""
    querystring.update(credentials)
    for item in request.param:
        querystring[item] = "bad credentials data"
    response = requests.request("POST", board_url, params=querystring)
    if response.status_code == HTTPStatus.OK:
        logger.info("****** Good credentials; TEST_BOARD created ******")
    else:
        logger.info("****** Bad credentials; can't login and create TEST_BOARD ******")
        logger.info(str(querystring))
    return response


@pytest.fixture()
def create_board_good(logger, credentials):
    """Create board with good credentials"""
    querystring.update(credentials)
    response = requests.request("POST", board_url, params=querystring)
    if response.status_code == HTTPStatus.OK:
        logger.info("****** Good credentials; TEST_BOARD created ******")
        logger.info(str(querystring))
    else:
        logger.info("****** Bad credentials; can't login and create TEST_BOARD ******")
    yield response
    board_url_get = URL + "members/me/boards"
    response = requests.request("GET", board_url_get, params=credentials)
    board_id, = [trello_board["id"] for trello_board in response.json() if trello_board["name"] == "TEST_BOARD"]
    board_url_del = URL + "/boards/"
    logger.info("Remove TEST_BOARD from Trello website")
    requests.request("DELETE", board_url_del + board_id, params=credentials)
