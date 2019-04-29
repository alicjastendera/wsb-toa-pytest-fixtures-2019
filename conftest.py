import pytest
import json
import logging
import requests

URL = "https://api.trello.com/1/"


@pytest.fixture(scope="session")
def credentials(logger):
    """Returns key and token required to authenticate against API"""
    logger.info("Preparing credentials")
    with open("credentials.json") as file:
        creds = json.load(file)
    logger.info(str(credentials))
    return creds


@pytest.fixture(scope="session")
def logger():
    """Returns logger object"""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("Logger")
    return logger
# https://stackoverflow.com/questions/4673373/logging-within-py-test-tests


@pytest.fixture()
def get_my_boards(credentials):
    """Returns dictionary with all user's boards"""
    boards_url = URL + "/members/me/boards"
    response = requests.get(boards_url, params=credentials)
    return response.json()
