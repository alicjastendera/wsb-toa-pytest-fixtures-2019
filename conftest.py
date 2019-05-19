import pytest
import json
import logging
import requests
from http import HTTPStatus

URL = "https://api.trello.com/1/"


@pytest.fixture(scope="session")
def credentials(logger):
    """Returns key and token required to authenticate against API"""
    logger.info("Preparing credentials")
    with open("..\credentials.json") as file:
        creds = json.load(file)
    logger.info(str(creds))
    return creds


@pytest.fixture(scope="session")
def logger():
    """Returns logger object"""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("Logger")
    return logger
# https://stackoverflow.com/questions/4673373/logging-within-py-test-tests


@pytest.fixture()
def create_empty_board(credentials, logger):
    """Creates empty board"""
    logger.info("Creating board with root fixture")
    boards_url = URL + "boards"
    querystring = {"name": "Not overriden root fixture used", "defaultLabels": "true", "defaultLists": "true",
                   "keepFromSource": "none", "prefs_permissionLevel": "private", "prefs_voting": "disabled",
                   "prefs_comments": "members", "prefs_invitations": "members", "prefs_selfJoin": "true",
                   "prefs_cardCovers": "true", "prefs_background": "blue", "prefs_cardAging": "regular"}

    querystring.update(credentials)
    response = requests.post(boards_url, params=querystring)

    if response.status_code == HTTPStatus.OK:
        logger.info("*********** Blue board created ***********")
    else:
        logger.error(response)

    yield response
    board_id = response.json()["id"]
    requests.delete(boards_url + "/" + board_id, params=credentials)


