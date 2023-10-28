from collections import namedtuple

Card = namedtuple('Card', ['value', 'suit'])


def check_if_string_is_card(string, valid_cards):
    split_string = string.split()
    if len(split_string) != 2:
        return False

    if Card(split_string[0], split_string[1]) in valid_cards:
        return True

    return False
