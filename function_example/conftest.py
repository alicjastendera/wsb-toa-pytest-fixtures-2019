import pytest
import json
import logging
import requests
import time
from http import HTTPStatus

URL = "https://api.trello.com/1/"
URL2 = "https://avwx.rest/api/metar/EPGD?options=&format=json&onfail=cache" # obserwacja pogodowa dla lotniska w Gdańsku


@pytest.fixture(scope="session")
def credentials(logger):
    logger.info("Preparing credentials")
    with open("credentials.json") as file:
        creds = json.load(file)
    logger.info(str(credentials))
    return creds


@pytest.fixture(scope="session")
def logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Logger")
    return logger
# https://stackoverflow.com/questions/4673373/logging-within-py-test-tests


@pytest.fixture()
def create_board(credentials, logger):
    board_ids = []
    logger.info("Creating board")
    boards_url = URL + "boards"
    querystring = {"name": "AVIATION WEATHER", "defaultLabels": "false", "defaultLists": "false",
                   "prefs_background": "blue"}

    querystring.update(credentials)
    response = requests.post(boards_url, params=querystring)
    logger.info(response.text)
    board_id = response.json()["id"]
    board_ids.append(board_id)
    yield board_id

    logger.info("Removing '{}' board after test".format(id))
    requests.delete(boards_url + "/" + board_id, params=credentials)
    return


@pytest.fixture()
def create_lists(credentials, logger, create_board, aviation_weather):
    logger.info("Creating lists")
    lists_url = URL + "lists"
    querystring = {"name": aviation_weather[1], "idBoard": create_board}
    querystring.update(credentials)
    response = requests.post(lists_url, params=querystring)
# Time sleep z uwagi na możliwość podglądu w UI TRELLO tworzenia listy z informacją pogodową tzw. "metar"
    time.sleep(5)
    return response


@pytest.fixture()
def aviation_weather(logger):
    logger.info("Download metar info")
    metar_url = URL2
    body = {}
# Lotnicza informacja pogodowa dla lotniska to tzw. "metar" czyli zakodowana informacja łatwo interpretowalna przez
# pilotów i uaktualniana co 30min. Na potrzeby tego testu "metar" pobierany jest z Lotniska Rębiechowo(skrót ICAO: EPGD)
    response = requests.get(metar_url, params=body)
    logger.info(response.text)
    metar_item = response.json()["raw"]
    if response.status_code == HTTPStatus.OK:
        logger.info(metar_item)
    return response, metar_item


