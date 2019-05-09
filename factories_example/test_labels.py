from helper import get_users_boards


class TestLabels:

    def test_create_cards_with_label(self, create_board_factory, create_list_factory, create_label_on_a_board,
                                     create_card_factory):
        """Creates "WEDDING" board, creates 3 lists on it: "TO DO". On "TO DO" list creates
        cards: "Invitations", "Flowers" and "Fireworks" with different labels"""
        board_id = create_board_factory("WEDDING")
        list_id = create_list_factory(board_id, "TO DO")

        green_label = create_label_on_a_board("Medium important", "green", board_id)
        yellow_label = create_label_on_a_board("Very important", "yellow", board_id)
        red_label = create_label_on_a_board("Extremely important", "red", board_id)

        card_green = create_card_factory("Invitations", list_id, green_label["id"])
        card_red = create_card_factory("Flowers", list_id, red_label["id"])
        card_yellow = create_card_factory("Fireworks", list_id, yellow_label["id"])

        assert card_green["labels"][0]["color"] == "green"
        assert card_red["labels"][0]["color"] == "red"
        assert card_yellow["labels"][0]["color"] == "yellow"

    def test_create_3_boards(self, credentials, create_board_factory):
        """Try to create 3 boards"""
        create_board_factory("First board")
        create_board_factory("Second board")
        create_board_factory("Third board")

        response = get_users_boards(credentials)
        open_boards = [board["name"] for board in response.json() if board["closed"] is False]

        assert len(open_boards) == 3



