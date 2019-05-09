import pytest
import requests
import time
from http import HTTPStatus

URL = "https://api.trello.com/1/"
URL_AVWX = "https://avwx.rest/api/metar/EPGD?options=&format=json&onfail=cache" # Weather observation for the Gdańsk airport


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
def create_list(credentials, logger, create_board, get_aviation_weather):
    logger.info("Creating list")
    list_url = URL + "lists"
    querystring = {"name": get_aviation_weather[1], "idBoard": create_board}
    querystring.update(credentials)
    response = requests.post(list_url, params=querystring)
    # Time sleep due to the possibility of viewing in TRELLO UI a list with weather information "metar"
    time.sleep(5)
    return response


@pytest.fixture()
def get_aviation_weather(logger):
    logger.info("Download metar info")
    metar_url = URL_AVWX
    body = {}
    # Aeronautical weather information for the airport is called "metar" that is coded information easily interpretable
    # by pilots and updated every 30 min. For the purposes of this test, the "metar" is collected from the Rębiechowo
    # Airport (abbreviated ICAO: EPGD)
    response = requests.get(metar_url, params=body)
    logger.info("metar for Gdańsk - Rębiechowo:")
    logger.info(response.text)
    metar_item = response.json()["raw"]
    if response.status_code == HTTPStatus.OK:
        logger.info(metar_item)
    return response, metar_item


