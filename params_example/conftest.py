import pytest
import json

URL = "https://api.trello.com/1/"


@pytest.fixture(scope="session", params=["params_example\wrong_key.json", "params_example\wrong_token.json",
                                         "params_example\\all_wrong.json"])
def bad_credentials(request, logger):
    """Returns incorrect key and token"""
    logger.info("Preparing incorrect credentials")
    with open(request.param) as file:
        creds = json.load(file)
    logger.info("Loaded credentials: {}".format(creds))
    return creds
