import json
import pytest
import requests
from http import HTTPStatus

URL = "https://api.trello.com/1/"


board_url = URL + "boards"

querystring = {"name":"test","defaultLabels":"false","defaultLists":"false","keepFromSource":"none",
               "prefs_permissionLevel":"private","prefs_voting":"disabled","prefs_comments":"members",
               "prefs_invitations":"members","prefs_selfJoin":"true","prefs_cardCovers":"true",
               "prefs_background":"blue","prefs_cardAging":"regular","key":"6fd7c30f4c4c3d2b010eb79b4266463f",
               "token":"5bffe9b7599d4a881b03e420017912becb77ce8c968d22a0b4bba5b793dc6220"}

response = requests.request("POST", board_url, params=querystring)

print(response.text)


querystring_two = {"key":"6fd7c30f4c4c3d2b010eb79b4266463f",
               "token":"5bffe9b7599d4a881b03e420017912becb77ce8c968d22a0b4bba5b793dc6220"}


board_url_get = URL + "members/me/boards"
response = requests.get(board_url_get, params=querystring_two)
board_id = [trello_board["id"] for trello_board in response.json() if trello_board["name"] == "test"]


print(board_id)




# lists_url = URL + "/boards/{}/lists".format(board_id)
# response = requests.get(lists_url, params=trello_creds)
# list_id, = [trello_list["id"] for trello_list in response.json() if trello_list["name"] == "pytest-list"]
# return list_id


#
# url = "https://api.trello.com/1/boards/board_id"
#
# querystring = {"key":"6fd7c30f4c4c3d2b010eb79b4266463f","token":"5bffe9b7599d4a881b03e420017912becb77ce8c968d22a0b4bba5b793dc6220"}
#
# response = requests.request("DELETE", url, params=querystring)
#
# print(response.text)