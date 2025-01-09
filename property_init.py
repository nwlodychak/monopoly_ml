import pandas as pd
from dataclasses import dataclass, field
from monopoly_ml.player import Player


@dataclass
class Space:
    # This is used for spaces that fall under non-defined categories, e.g jail, go, etc.
    name: str
    position: int
    result: str
    cost: int
    jail_status: bool
    space_change: int or None


@dataclass
class Street:
    # This is used for standard properties
    name: str
    position: int
    color_group: str
    cost_to_buy: int
    house_cost: int
    rent: int
    one_house: int
    two_house: int
    three_house: int
    four_house: int
    hotel: int
    owner: str = None
    mortgage_status: bool = False
    house_status: int = 0
    hotel_status: int = 0
    def __post_init__(self):
        self.mortgage = int(0.5 * self.cost_to_buy)
        self.unmortgage = int(self.mortgage + (0.1 * self.mortgage))

def get_properties():
    df = pd.read_csv('data/streets_metaval.csv')
    props = {row['name']: Street(**row) for row in df.to_dict('records')}
    return props


@dataclass
# This is used for community chest and chance cards
class Card:
    name: str
    type: str
    text: str
    cost: int
    jail_status: bool
    space_change: int or None


def get_board():
    board = [{'name': 'go', 'type': 'space'},
             {'name': 'mediterranean avenue', 'type': 'street'},
             {'name': 'community chest', 'type': 'card'},
             {'name': 'baltic avenue', 'type': 'street'},
             {'name': 'income tax', 'type': 'space'},
             {'name': 'reading railroad', 'type': 'property'},
             {'name': 'oriental avenue', 'type': 'street'},
             {'name': 'chance', 'type': 'card'},
             {'name': 'vermont avenue', 'type': 'street'},
             {'name': 'connecticut avenue', 'type': 'street'},
             {'name': 'jail', 'type': 'space'},
             {'name': 'st charles place', 'type': 'street'},
             {'name': 'electric company', 'type': 'property'},
             {'name': 'states avenue', 'type': 'street'},
             {'name': 'virginia avenue', 'type': 'street'},
             {'name': 'pennsylvania railroad', 'type': 'property'},
             {'name': 'st james place', 'type': 'street'},
             {'name': 'community chest', 'type': 'card'},
             {'name': 'tennessee avenue', 'type': 'street'},
             {'name': 'new york avenue', 'type': 'street'},
             {'name': 'free parking', 'type': 'space'},
             {'name': 'kentucky avenue', 'type': 'street'},
             {'name': 'chance', 'type': 'card'},
             {'name': 'indiana avenue', 'type': 'street'},
             {'name': 'illinois avenue', 'type': 'street'},
             {'name': 'b&o railroad', 'type': 'property'},
             {'name': 'atlantic avenue', 'type': 'street'},
             {'name': 'ventnor avenue', 'type': 'street'},
             {'name': 'water works', 'type': 'property'},
             {'name': 'marvin gardens', 'type': 'street'},
             {'name': 'go_to_jail', 'type': 'space'},
             {'name': 'pacific avenue', 'type': 'street'},
             {'name': 'north carolina avenue', 'type': 'street'},
             {'name': 'community chest', 'type': 'card'},
             {'name': 'pennsylvania avenue', 'type': 'street'},
             {'name': 'short line railroad', 'type': 'property'},
             {'name': 'chance', 'type': 'card'},
             {'name': 'park place', 'type': 'street'},
             {'name': 'luxury tax', 'type': 'space'},
             {'name': 'boardwalk', 'type': 'street'}
             ]
    return board


def get_bank():
    dict_bank = {'cash'  : 5000,
                 'houses': 32,
                 'hotels': 12}
    return dict_bank



def get_community_chest_cards(player):
    return [
        Card("stock_sale", "community_chest", "FROM SALE OF STOCK YOU GET 50.", 50, False, None),
        Card("birthday", "community_chest", "IT'S YOUR BIRTHDAY. COLLECT 10 FROM EACH PLAYER.", 10, False, None),
        ## todo change this to work for players
        Card("holiday_fund", "community_chest", "HOLIDAY FUNC MATURES. COLLECT 100", 100, False, None),
        Card("hospital_fees", "community_chest", "HOSPITAL FEES. PAY 100.", -100, False, None),
        Card("second_price", "community_chest", "YOU HAVE WON SECOND PRIZE IN A BEAUTY CONTEST. COLLECT 100", 100,
             False, None),
        Card("school_fees", "community_chest", "SCHOOL FEES. PAY 50.", -50, False, None),
        Card("jail", "community_chest", "GO TO JAIL. GO DIRECTLY TO JAIL. DO NOT PASS GO. DO NOT COLLECT 200.", 100,
             True, 10),
        Card("consultancy", "community_chest", "COLLECT 25 CONSULTANCY FEE.", 25, False, None),
        Card("income_tax", "community_chest", "INCOME TAX REFUND. COLLECT 20.", 20, False, None),
        Card("insurance", "community_chest", "LIFE INSURANCE MATURES. COLLECT 100", 100, False, None),
        Card("bank_error", "community_chest", "BANK ERROR IN YOUR FAVOUR. COLLECT 200.", 200, False, None),
        Card("doctor_fees", "community_chest", "DOCTOR'S FEES. PAY 50.", -50, False, None),
        Card("to_go", "community_chest", "ADVANCE TO GO. COLLECT 200.", 100, False, 0),
        Card("doctor_fees", "community_chest", "YOU INHERIT 100.", 100, False, None),
        Card("street_repair", "community_chest", "YOU ARE ASSESSED FOR STREET REPAIRS: "
                                                 "PAY 40 PER HOUSE AND 115 PER HOTEL YOU OWN.",
             (player._dict_owned_houses * 40 + player._dict_owned_hotels * 115) * -1, False, None),
        Card("get_out_of_jail", "community_chest",
             "GET OUT OF JAIL FREE. THIS CARD MAY BE KEPT UNTIL NEEDED, TRADED OR SOLD.", 0, False, None)
    ]


def get_chance_cards(player):
    # todo edit in for chance cards
    return {
        Card("stock_sale", "community_chest", "FROM SALE OF STOCK YOU GET 50.", 50, False, None),
        Card("birthday", "community_chest", "IT'S YOUR BIRTHDAY. COLLECT 10 FROM EACH PLAYER.", 10, False, None),
        ## todo change this to work for players
        Card("holiday_fund", "community_chest", "HOLIDAY FUNC MATURES. COLLECT 100", 100, False, None),
        Card("hospital_fees", "community_chest", "HOSPITAL FEES. PAY 100.", -100, False, None),
        Card("second_price", "community_chest", "YOU HAVE WON SECOND PRIZE IN A BEAUTY CONTEST. COLLECT 100", 100,
             False, None),
        Card("school_fees", "community_chest", "SCHOOL FEES. PAY 50.", -50, False, None),
        Card("jail", "community_chest", "GO TO JAIL. GO DIRECTLY TO JAIL. DO NOT PASS GO. DO NOT COLLECT 200.", 100,
             True, 10),
        Card("consultancy", "community_chest", "COLLECT 25 CONSULTANCY FEE.", 25, False, None),
        Card("income_tax", "community_chest", "INCOME TAX REFUND. COLLECT 20.", 20, False, None),
        Card("insurance", "community_chest", "LIFE INSURANCE MATURES. COLLECT 100", 100, False, None),
        Card("bank_error", "community_chest", "BANK ERROR IN YOUR FAVOUR. COLLECT 200.", 200, False, None),
        Card("doctor_fees", "community_chest", "DOCTOR'S FEES. PAY 50.", -50, False, None),
        Card("to_go", "community_chest", "ADVANCE TO GO. COLLECT 200.", 100, False, 0),
        Card("doctor_fees", "community_chest", "YOU INHERIT 100.", 100, False, None),
        Card("street_repair", "community_chest", "YOU ARE ASSESSED FOR STREET REPAIRS: "
                                                 "PAY 40 PER HOUSE AND 115 PER HOTEL YOU OWN.",
             -((player._dict_owned_houses * 40) + (player._dict_owned_hotels * 115)), False, None),
        Card("get_out_of_jail", "community_chest",
             "GET OUT OF JAIL FREE. THIS CARD MAY BE KEPT UNTIL NEEDED, TRADED OR SOLD.", 0, False, None)
    }
