import requests


URL = "https://api.trello.com/1/"
USERS_BOARDS_URL = URL + "/members/me/boards"


def get_users_boards(credentials):
    querystring = {"filter": "all", "fields": "all", "lists": "none", "memberships": "none", "organization": "false",
                   "organization_fields": "name,displayName"}
    querystring.update(credentials)
    response = requests.get(USERS_BOARDS_URL, params=querystring)
    return response
