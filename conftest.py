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
    querystring = {"name": "Test board", "defaultLabels": "true", "defaultLists": "false",
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
    logger.info("Removing '{}' board after test".format(board_id))
    requests.delete(boards_url + "/" + board_id, params=credentials)


@pytest.fixture()
def create_empty_board_with_bcg_color(request, credentials, logger):
    """Creates empty board"""
    logger.info("Creating empty board")
    boards_url = URL + "boards"
    querystring = {"name": "Test board", "defaultLabels": "true", "defaultLists": "false",
                   "keepFromSource": "none", "prefs_permissionLevel": "private", "prefs_voting": "disabled",
                   "prefs_comments": "members", "prefs_invitations": "members", "prefs_selfJoin": "true",
                   "prefs_cardCovers": "true", "prefs_background": request.param, "prefs_cardAging": "regular"}

    querystring.update(credentials)
    response = requests.post(boards_url, params=querystring)

    if response.status_code == HTTPStatus.OK:
        logger.info(f"*********** {request.param} board created ***********")
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
        requests.delete(list_url + "/" + id, params=credentials)


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


@pytest.fixture()
def prepare_list_on_board(create_empty_board, create_list_factory, logger):
    """Prepares board "Test board" with one empty list "Test list". Returns whole response"""
    logger.info("Preparing board with one empty list.")
    return create_list_factory(create_empty_board.json()["id"], "Test list")


@pytest.fixture()
def create_card_and_list_on_board(prepare_list_on_board, credentials, logger):
    """Prepares board with one list on it and one card "Magic card" on it"""
    logger.info("Creating card on list: \"{}\" with list_id {} ".format(
                prepare_list_on_board.json()["name"], prepare_list_on_board.json()["id"]))
    card_url = URL + "cards"
    cards_ids = []
    card_name = "Magic card"
    querystring = {"idList": prepare_list_on_board.json()["id"], "name": card_name}  # TODO change to param
    querystring.update(credentials)
    response = requests.post(card_url, params=querystring)

    if response.status_code == HTTPStatus.OK:
        logger.info('"{}" card created'.format(card_name))
    else:
        logger.error(response)

    cards_ids.append(response.json()["id"])
    yield response

    for id in cards_ids:
        logger.info("Removing '{}' card after test".format(id))
        requests.delete(card_url + "/" + id, params=credentials)


@pytest.fixture()
def create_card_factory(logger, credentials):
    card_url = URL + "cards"
    card_ids = []

    def _create_card_factory(list_id, card_name, pos="bottom"):
        """Creates card on a given list with given name, position and returns its response"""
        querystring = {"name": card_name, "idList": list_id, "pos": pos}
        querystring.update(credentials)
        response = requests.post(card_url, params=querystring)
        if response.status_code == HTTPStatus.OK:
            logger.info('"{}" card created on list_id: {}'.format(card_name, list_id))
        else:
            logger.error(response)
        card_id = response.json()["id"]
        card_ids.append(card_id)
        return response

    yield _create_card_factory
    for id in card_ids:
        logger.info("Removing '{}' card after test".format(id))
        requests.delete(card_url + "/" + id, params=credentials)


@pytest.fixture()
def create_checkitem_on_checklist_factory(logger, credentials):
    def _create_checkitem_on_checklist_factory(checklist_id, checkitem_name, pos="bottom"):
        querystring = {"name": checkitem_name, "pos": pos}
        querystring.update(credentials)
        response = requests.post(URL + "checklists/" + checklist_id + "/checkItems", params=querystring)

        if response.status_code == HTTPStatus.OK:
            logger.info('"{}" checkitem created on checklist_id: {}'.format(checkitem_name, checklist_id))
        else:
            logger.error(response)
        return response
    yield _create_checkitem_on_checklist_factory
