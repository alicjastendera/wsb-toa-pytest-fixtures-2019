import requests

URL = "https://api.trello.com/1/"

querystring_two = {"key":"6fd7c30f4c4c3d2b010eb79b4266463f",
               "token":"5bffe9b7599d4a881b03e420017912becb77ce8c968d22a0b4bba5b793dc6220"}


board_url_get = URL + "members/me/boards"
response = requests.get(board_url_get, params=querystring_two)
board_id, = [trello_board["id"] for trello_board in response.json() if trello_board["name"] == "test"]

print(board_id)

board_url_del = URL + "/boards/"

response = requests.request("DELETE", board_url_del + board_id, params=querystring_two)

print(response.text)