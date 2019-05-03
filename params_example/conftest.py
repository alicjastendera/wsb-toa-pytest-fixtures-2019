import requests
import pytest
import json
import linecache
import os

from http import HTTPStatus

URL = "https://api.trello.com/1/"

board_url = URL + "boards"
querystring = {"name": "TEST_BOARD", "defaultLabels": "true", "default": "true", "keepFromSource": "none",
                   "prefs_permissionLevel": "private", "prefs_voting": "disabled", "prefs_comments": "members",
                   "prefs_invitations": "members", "prefs_selfJoin": "true", "prefs_cardCovers": "true",
                   "prefs_background": "pink", "prefs_cardAging": "regular"}


@pytest.fixture(scope="session")
def crate_bad_credentials(logger):
    """Create and delete bad credentials files based on good credentials file"""
    creds_kay = linecache.getline("credentials.json", 2)
    creds_token = linecache.getline("credentials.json", 3)

    open("wrong_token.json", "w").write("{\n" + creds_kay + '  "token":"Wrong_token"\n' + "}")
    logger.info("Creating credential file with bad TOKEN")
    open("wrong_key.json", "w").write("{\n" + '  "key":"Wrong_key",\n' + creds_token + "}")
    logger.info("Creating credential file with bad KEY")
    open("all_wrong.json", "w").write("{\n" + '  "key":"Wrong_key",\n' + '  "token":"Wrong_token"\n' + "}")
    logger.info("Creating credential file with bad TOKEN and KEY")
    yield
    os.remove("wrong_token.json")
    logger.info("Remove credential file with bad TOKEN")
    os.remove("wrong_key.json")
    logger.info("Remove credential file with bad KEY")
    os.remove("all_wrong.json")
    logger.info("Remove credential file with bad TOKEN and KEY")


@pytest.fixture(scope="session", params=["wrong_token.json", "wrong_key.json", "all_wrong.json"])
def bad_credentials(request, logger):
    """Returns incorrect key and token"""
    logger.info("Preparing incorrect credentials")
    with open(request.param) as file:
        creds = json.load(file)
    logger.info("Loaded credentials: {}".format(creds))
    return creds


@pytest.fixture()
def create_board_bad(crate_bad_credentials, logger, bad_credentials):
    """Try create board with bad credentials"""
    querystring.update(bad_credentials)
    response = requests.request("POST", board_url, params=querystring)
    if response.status_code == HTTPStatus.OK:
        logger.info("****** Good credentials; TEST_BOARD created ******")
    else:
        logger.info("****** Bad credentials; can't login and create TEST_BOARD ******")
    return response


@pytest.fixture()
def create_board_good(logger, credentials):
    """Create board with good credentials"""
    querystring.update(credentials)
    response = requests.request("POST", board_url, params=querystring)
    if response.status_code == HTTPStatus.OK:
        logger.info("****** Good credentials; TEST_BOARD created ******")
    else:
        logger.info("****** Bad credentials; can't login and create TEST_BOARD ******")
    yield response
    board_url_get = URL + "members/me/boards"
    response = requests.request("GET", board_url_get, params=credentials)
    board_id, = [trello_board["id"] for trello_board in response.json() if trello_board["name"] == "TEST_BOARD"]
    board_url_del = URL + "/boards/"
    logger.info("Remove TEST_BOARD from Trello website")
    requests.request("DELETE", board_url_del + board_id, params=credentials)
