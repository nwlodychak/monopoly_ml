class Player:
    def __init__(self, name, number, bank, list_board, dict_roads, dict_properties, community_cards_deck):
        self._name = name
        self._number = number
        self._list_board = list_board
        self._dict_all_properties = dict_properties
        self._position = 0
        self._dice_value = 0
        self._cash = 1500
        self._properties_total_mortgageable_amount = 0
        self._get_out_of_jail_cards = False  # holds card to exit jail
        self._jail_count = 0
        self._free_visit = False
        self._bank = bank
        self._list_players = None
        self._dict_players = None
        self._list_owned_properties = []
        self._list_mortgaged_properties = []
        self._dict_owned_colors = {'brown': False, 'light_blue': False, 'purple': False, 'orange': False,
                                   'red'  : False, 'yellow': False, 'green': False, 'blue': False}
        self._dict_owned_houses = {}
        self._dict_owned_hotels = {}
        self._has_lost = False
        self.color_to_house_mapping = get_color_to_house_mapping()