from http import HTTPStatus
from helper import get_users_boards


class TestLabels:

    def test_create_label_on_a_board(self, credentials, create_empty_board, create_list_factory,
                                     create_label_on_a_board_factory):
        board_response = get_users_boards(credentials)
        board_id = [board["id"] for board in board_response.json() if board["closed"] is False]

        assert create_list_factory(board_id, "TO DO").status_code
        assert create_label_on_a_board_factory("Urgent", "pink", board_id).status_code == HTTPStatus.OK
