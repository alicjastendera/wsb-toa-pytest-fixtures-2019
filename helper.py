import requests
from conftest import URL


def get_users_boards(credentials):
    users_boards_url = URL + "/members/me/boards"
    querystring = {"filter": "all", "fields": "all", "lists": "none", "memberships": "none", "organization": "false",
                   "organization_fields": "name,displayName"}
    querystring.update(credentials)
    response = requests.get(users_boards_url, params=querystring)
    return response
