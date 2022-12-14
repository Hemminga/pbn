import string
import types
from pprint import pprint


def process_pbn_input(pbn: string):
    base = types.SimpleNamespace()  # Object
    dealer_raw, hand_raw = process_raw_input(pbn)
    base.dealer_raw = dealer_raw
    base.pbn = pbn
    base.hand_raw = hand_raw
    dealer = get_dealer(dealer_raw)
    base.dealer = dealer
    hands = [x.strip() for x in hand_raw.split(' ')]
    assert len(hands) == 4, \
        f"Expected four hands in PBN string, got {len(hands)} instead."
    assert [len(x) for x in hands] == [16, 16, 16, 16], \
        f"Expected each hand to be of length 16 (13 cards and 3 dots.) Got {[len(x) for x in hands]} instead."
    # hands, dealer, rotated_pbn = rotate_hands(hands, dealer)
    rotated_hands = rotate_hands(hands, dealer)
    rotated_pbn = "N:" + ' '.join([rotated_hands[x] for x in range(0, 4)])
    base.dealer = dealer
    pbn_english, pbn_dutch = translate_pbn(rotated_pbn)
    base.pbn = pbn_english
    base.pbn_dutch = pbn_dutch
    hands = convert_into_hands(pbn_dutch)
    base.hands = hands
    return base


def process_raw_input(raw_input: string) -> (string, string):
    """Takes raw user input and starts processing by taking the first two characters
    as dealer and the tail as raw PBN.
    Does some preliminary sanity checks.
    :rtype: tuple
    :param raw_input:
    :return: """
    raw_input = raw_input.upper()
    dealer_raw = raw_input[:2]
    print(f"dealer_raw: {dealer_raw}")
    assert raw_input[1] == ':' and raw_input[0].upper() in ["N", "E", "S", "W", "O", "Z"], \
        f"Malformed start of PBN string. got `{dealer_raw}` expecting `[NESWOZ]:`"
    hand_raw = raw_input[2:]
    assert len(hand_raw) == 67, \
        f"A few cards may be missing. Got `len(hand_raw) == {len(hand_raw)}`, expecting 67"
    print(f"hand_raw: {hand_raw}")
    return dealer_raw, hand_raw


def get_dealer(dealer_raw: string) -> string:
    """Extracts dealer from
    :rtype: string
    :param dealer_raw:
    :return:
    """
    this_dealer = dealer_raw[0].upper()
    # Correct Dutch notation of South and East.
    # If this ever gets relevant refactor this out into a separate
    # function dealing with more languages.
    if this_dealer == 'Z':
        this_dealer = 'S'
    if this_dealer == 'O':
        this_dealer = 'E'
    assert this_dealer in ["N", "E", "S", "W"], \
        f"Expected dealer to be in ['N', 'E', 'S', 'W'], got {this_dealer} instead"
    return this_dealer


def rotate_hands(hands, dealer):
    """Rotates the raw input PBN hands to make the first hand 'N'
    @param hands: list
    @param dealer: string
    @return:

    """
    rotate = 0
    if dealer == 'E':
        rotate = 1
    elif dealer == 'S':
        rotate = 2
    elif dealer == 'W':
        rotate = 3
    rotated_hands = {}
    for i in range(0, 4):
        rotated_hands[i] = hands[(i + rotate) % 4]
    return rotated_hands


def convert_into_hands(rotated_pbn):
    bare_pbn = rotated_pbn[2:]
    hands = [x.strip() for x in bare_pbn.split(' ')]
    hands_as_object = types.SimpleNamespace()  # Object
    north = hands[0].split('.')
    hands_as_object.north = types.SimpleNamespace(
        spades=north[0], hearts=north[1], diamonds=north[2], clubs=north[3])
    east = hands[1].split('.')
    hands_as_object.east = types.SimpleNamespace(
        spades=east[0], hearts=east[1], diamonds=east[2], clubs=east[3])
    south = hands[2].split('.')
    hands_as_object.south = types.SimpleNamespace(
        spades=south[0], hearts=south[1], diamonds=south[2], clubs=south[3])
    west = hands[3].split('.')
    hands_as_object.west = types.SimpleNamespace(
        spades=west[0], hearts=west[1], diamonds=west[2], clubs=west[3])
    return hands_as_object


def translate_pbn(hand_raw):
    # From Dutch to English
    pbn_english = hand_raw
    pbn_dutch = hand_raw
    replacements = {
        'H': 'K',
        'V': 'Q',
        'B': 'J',
        'O': 'E',
        'Z': 'S'
    }
    for dutch, english in replacements.items():
        pbn_english = pbn_english.replace(dutch, english)
        pbn_dutch = pbn_dutch.replace(english, dutch)
    print(f"pbn_dutch: {pbn_dutch}")
    return pbn_english, pbn_dutch
