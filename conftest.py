import pytest
import json
import os
import logging
import requests
from http import HTTPStatus
from helper import get_users_boards

URL = "https://api.trello.com/1/"


@pytest.fixture(scope="session")
def credentials(logger):
    """Returns key and token required to authenticate against API"""
    logger.info("Preparing credentials")
    conftest_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(conftest_path, "credentials.json")) as file:
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
    logger.info("Creating empty board")
    boards_url = URL + "boards"
    querystring = {"name": "Test board", "defaultLabels": "true", "defaultLists": "true",
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


@pytest.fixture()
def create_empty_board_with_bcg_color(request, credentials, logger):
    """Creates empty board"""
    logger.info("Creating empty board")
    boards_url = URL + "boards"
    querystring = {"name": "Test board", "defaultLabels": "true", "defaultLists": "true",
                   "keepFromSource": "none", "prefs_permissionLevel": "private", "prefs_voting": "disabled",
                   "prefs_comments": "members", "prefs_invitations": "members", "prefs_selfJoin": "true",
                   "prefs_cardCovers": "true", "prefs_background": request.param, "prefs_cardAging": "regular"}

    querystring.update(credentials)
    response = requests.post(boards_url, params=querystring)

    if response.status_code == HTTPStatus.OK:
        logger.info("*********** Blue board created ***********")
    else:
        logger.error(response)

    yield response, request.param
    board_id = response.json()["id"]
    requests.delete(boards_url + "/" + board_id, params=credentials)


@pytest.fixture(autouse=True, scope="function")
def remove_boards_before_test(logger, credentials):
    response = get_users_boards(credentials)
    open_boards = [board["id"] for board in response.json() if board["closed"] is False]
    if len(open_boards) != 0:
        boards_url = URL + "boards"
        for id in open_boards:
            logger.info("Removing old boards before test")
            requests.delete(boards_url + "/" + id, params=credentials)


@pytest.fixture()
def create_board_factory(logger, credentials):
    board_ids = []
    boards_url = URL + "boards"

    def _create_board_factory(board_name):
        """Creates board with given name parameter and returns its id"""
        logger.info("Creating '{}' board".format(board_name))
        querystring = {"name": board_name, "defaultLabels": "true", "defaultLists": "false"}
        querystring.update(credentials)
        response = requests.post(boards_url, params=querystring)

        if response.status_code == HTTPStatus.OK:
            logger.info("*********** Board created ***********")
        else:
            logger.error(response)
        board_id = response.json()["id"]
        board_ids.append(board_id)
        return board_id
    yield _create_board_factory
    for id in board_ids:
        logger.info("Removing '{}' board after test".format(id))
        requests.delete(boards_url + "/" + id, params=credentials)


@pytest.fixture()
def create_list_factory(logger, credentials):
    list_url = URL + "lists"
    lists_ids = []

    def _create_list_factory(board_id, list_name):
        """Creates list on a given board with given name parameter and returns its id"""
        querystring = {"name": list_name, "idBoard": board_id}
        querystring.update(credentials)
        response = requests.post(list_url, params=querystring)
        if response.status_code == HTTPStatus.OK:
            logger.info('"{}" list created'.format(list_name))
        else:
            logger.error(response)
        list_id = response.json()["id"]
        lists_ids.append(list_id)
        return response

    yield _create_list_factory
    for id in lists_ids:
        logger.info("Removing '{}' list after test".format(id))
        requests.put(list_url + "/" + id, params=credentials)

    return _create_list_factory


@pytest.fixture()
def create_label_on_a_board_factory(logger, credentials):
    def _create_label_on_a_board(label_name, label_color, board_id):
        """Creates label on a given board"""
        label_url = URL + "labels"
        querystring = {"name": label_name, "color": label_color, "idBoard": board_id}
        querystring.update(credentials)
        response = requests.post(label_url, params=querystring)
        if response.status_code == HTTPStatus.OK:
            logger.info('"{}" label created'.format(label_name))
        else:
            logger.error(response)

        return response
    return _create_label_on_a_board
