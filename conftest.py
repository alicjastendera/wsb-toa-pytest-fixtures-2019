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
def create_board(credentials, logger):
    """Returns dictionary with all user's boards"""
    logger.info("Creating board")
    boards_url = URL + "boards"
    querystring = {"name": "Shopping", "defaultLabels": "true", "defaultLists": "true", "keepFromSource": "none",
                   "prefs_permissionLevel": "private", "prefs_voting": "disabled", "prefs_comments": "members",
                   "prefs_invitations": "members", "prefs_selfJoin": "true", "prefs_cardCovers": "true",
                   "prefs_background": "blue", "prefs_cardAging": "regular"}

    querystring.update(credentials)
    print(querystring)
    response = requests.post(boards_url, params=querystring)

    if response.status_code == HTTPStatus.OK:
        logger.info("*********** Board created ***********")
    else:
        logger.error(response)
    return response
