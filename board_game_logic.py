import random
from collections import namedtuple
from tokenize import group

from sympy.physics.quantum.shor import ratioize
# from monopoly_ml.player import Player
from sympy.stats.rv import probability
from monopoly_ml.property_init import Street, get_board, get_community_chest_cards, get_chance_cards, get_properties


def dice_roll():
    """
    Random die roll for two dice. Returns the result and whether or not it is doubles
    :return:
    """
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    roll_result = namedtuple(typename = 'roll', field_names = ['total', 'doubles'])
    return roll_result(total = die1 + die2, doubles = True if die1 == die2 else False)


def jail(player, roll_count):
    if player._get_out_of_jail_cards is not False:
        player._get_out_of_jail_cards = False
        player._jail_status = False
    else:
        if roll_count < 3:
            dice = dice_roll()
            player._jail_count += 1
            if dice.doubles:
                player._jail_status = False
                player._jail_count == 0
        elif roll_count == 3:
            dice = dice_roll()
            if dice.doubles:
                player._jail_status = False
                player._jail_count == 0
            else:
                player._jail_status = False
                player._cash -= 50 # Pay $50 to get out
                player._jail_count == 0

def draw_card(player):
    space = get_board()[player._position]
    if space['name'] == 'community chest':
        community_cards = get_community_chest_cards(player)
        card = random.choice(community_cards)
    elif space['name'] == 'chance': ## Todo change this fucntion
        chance_cards = get_chance_cards(player)
        card = random.choice(chance_cards)
    else:
        print("Not a card space, something is wrong!")
    print(card)


def mortgage_property(player, rent):
    ## todo can we make logic to allow for purchase of hotels with mortgaging - ideally house purchase is winning
    ## strategy when we dont have all of another color

    amount_needed = rent - player._cash
    def min_subset_sum(values, target):
        dp = [float('inf')] * (target + 1)
        dp[0] = 0

        for i in range(1, target + 1):
            for value in values:
                if value <= i:
                    dp[i] = min(dp[i], dp[i - value] + 1)

        return dp[target] if dp[target] != float('inf') else -1

    min_subset_sum(player._dict_all_properties, amount_needed)


def calculate_street_rent(property, owner):
    rent_levels = [
        property.rent,
        property.one_house,
        property.two_house,
        property.three_house,
        property.four_house,
        property.hotel
    ]

    if owner._dict_owned_hotels[property]:
        return rent_levels[-1]

    if owner.dict_owned_houses[property]:
        return rent_levels[owner.dict_owned_houses[property]]

    if owner._dict_owned_colors[property.color_group]:
        return rent_levels[0] * 2

    return rent_levels[0]


def calculate_railroad_rent(property, owner):
    """
    Handles rent based on accumulation of railroads
    :param property: Not needed but keeps the function schema consistent
    :param owner: property owner
    :return: rent
    """
    rent_levels = [
        property.rent,
        property.rent_with_two,
        property.rent_with_three,
        property.rent_with_four
    ]
    return rent_levels[len(owner._list_owned_railroads) - 1]


def calculate_utility_rent(property, owner):
    """
    Handles rent based on a dice roll specifically for utilities
    :param property: Not needed but keeps the function schema consistent
    :param owner:
    :return: rent
    """
    rent_levels = [
        4,
        10
    ]
    roll = dice_roll().total
    return rent_levels[len(owner._list_owned_utilities) - 1] * roll


def pay_rent(player, property):
    """
    Handles rent payment logic based on property type and ownership status.
    Updates player and owner cash balances accordingly.
    :param player: player that landed on tile
    :param property: property corresponding to the tile.
    """
    if property.mortgage_status:
        return

    owner = property.owner
    current_rent = 0

    rent_calculators = {
        "street"  : calculate_street_rent,
        "railroad" : calculate_railroad_rent,
        "utilities" : calculate_utility_rent
    }

    calculator = rent_calculators.get(property.type)
    if not calculator:
        raise ValueError("Invalid property type")

    current_rent = calculator(property, owner)

    if player._cash < current_rent:
        # TODO: Implement bankruptcy handling
        # sell_houses()
        # mortgage_properties()
        return

    player._cash -= current_rent
    owner._cash += current_rent


def landing_on_property(player, property):
    probability_of_purchase = 0.9
    probability_of_purchase_with_one = 1
    if property.owner == None:
        if random.random() < probability_of_purchase and player.cash >= property.cost:
            player._cash -= property.cost
            property.owner = player
            if property.type == Street:
                player._list_owned_streets.append(property)

        else:
            auction_property(property, players)
            ### we do not purchase and it goes to auction
    else:
        pay_rent(player, property)


def auction_property(property, players):
    """
    This function is logic for auctioning properties. All players are allowed to bid.
    If a player owns properties in the group it is very likely they will purchase the property.
    The auction ends when a player has outbid everyone else and there is only one active bidder
    :param property: The property being auctioned
    :param players: all bidding players
    :return: cost of purchasing auctioned property and auction winner
    """

    current_price = property.cost_to_buy
    bid_increment = property.cost_to_buy * 0.1  # base bid increment

    def _probability_of_raise(player, current_price):
        """
        Helper function to assign raising probability for a property
        :param player:
        :param current_price:
        :return:
        """
        if type(property) == Street:
            if property.color_group in player._dict_owned_colors:
                p_int = 0.99  # if we have a color group highly likely to purchase
            else:
                p_int = 0.5  # if we don't less likely to purchase

        else:
            if property.type == 'utility' and len(player._list_owned_utilites) > 0:
                p_int = 0.95
            elif property.type == 'railroad' and len(player._list_owned_railroads) > 0:
                p_int = 0.95
            else:
                p_int = 0.5

        cash_ratio = current_price / player._cash
        p_bid = (p_int * max(0.2, 1 - cash_ratio))
        if p_bid < 0.2:
            p_bid = 0.2
        return p_bid

    active_bidders = players.copy()
    current_winner = None

    while len(active_bidders) > 1:
        remaining_bidders = []
        for bidder in active_bidders:
            p_bid = _probability_of_raise(bidder, current_price)
            # Random choice weighted by probability
            if random.random() < p_bid:
                # Calculate bid increase based on remaining cash
                max_increase = min(
                        bidder._cash - current_price,  # Can't bid more than cash
                        bid_increment * (1 + p_bid)  # Higher probability = more aggressive
                )
                if max_increase > 0:
                    remaining_bidders.append(bidder)
                    current_winner = bidder

        active_bidders = remaining_bidders
        if remaining_bidders:
            current_price += bid_increment
        if current_winner == None:
            return ("NoWinner", current_price)
    return (current_winner._name, current_price)


def calculate_trade_probability(player, opposing_player, property_offered, property_wanted = None, money_offered = 0):
    """
    This function calculates the probability of a trade being completed in monopoly
    :param player:
    :param opposing_player:
    :param property_offered:
    :param property_wanted:
    :param money_offered:
    :return:
    """
    # Constants for probability weights
    BASE_PROB = 0.3
    MONOPOLY_WEIGHT = 0.8
    MONEY_WEIGHT = 0.2


    def _get_property_ratio(player, property):
        """
        helper function to get property to monopoly ratio
        :param player: player of interest
        :param property: property of interest
        :return: ratio of properties to monopoly
        """
        property_color = property.color_group
        player_in_group = sum(1 for p in player._list_owned_streets
                              if p.color_group == property_color)
        total_in__group = sum(1 for p in get_properties().values()
                              if p['color_group'] == property_color)
        return player_in_group / total_in__group

    # Calculate base probability
    player_ratio = _get_property_ratio(player, property_offered.color_group)
    opponent_ratio = _get_property_ratio(opposing_player, property_offered.color_group)

    opponent_willingness = opponent_ratio - player_ratio
    player_desire = player_ratio - opponent_ratio

    # Initial trade probability
    p_trade = BASE_PROB * (1 - player_ratio) * opponent_ratio

    # Adjust for monopoly potential
    if property_wanted:
        monopoly_potential = (get_property_ratio(opposing_player,
                                                 property_wanted.color) == 1)
        if monopoly_potential:
            p_trade *= (1 + MONOPOLY_WEIGHT)

    # Adjust for money incentive
    if money_offered > 0:
        money_factor = min(money_offered / property_offered.price, 2)
        p_trade *= (1 + MONEY_WEIGHT * money_factor)

    return min(1.0, max(0.1, p_trade))


def execute_trade(player, opposing_player, property_offered,
                  property_wanted = None, money_offered = 0):
    """
    Execute the trade between players if probability threshold is met
    """
    p_trade = calculate_trade_probability(player, opposing_player,
                                          property_offered, property_wanted,
                                          money_offered)

    if random.random() < p_trade:
        # Execute property exchange
        player._list_owned_streets.remove(property_offered)
        opposing_player._list_owned_streets.append(property_offered)

        if property_wanted:
            opposing_player._list_owned_streets.remove(property_wanted)
            player._list_owned_streets.append(property_wanted)

        if money_offered > 0:
            player.money -= money_offered
            opposing_player.money += money_offered

        return True

    return False
