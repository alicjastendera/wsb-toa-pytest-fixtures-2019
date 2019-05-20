import requests
import pytest
from http import HTTPStatus

URL = "https://api.trello.com/1/"


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
