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

