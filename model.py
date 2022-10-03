import string
from pprint import pprint


def process_pbn_input(pbn: string):
    dealer_raw, hand_raw = process_raw_input(pbn)
    dealer = get_dealer(dealer_raw)
    hands = [x.strip() for x in hand_raw.split(' ')]
    assert len(hands) == 4, \
        f"Expected four hands in PBN string, got {len(hands)} instead."
    assert [len(x) for x in hands] == [16, 16, 16, 16], \
        f"Expected each hand to be of length 16 (13 cards and 3 dots.) Got {[len(x) for x in hands]} instead."
    pprint(hands)


def process_raw_input(raw_input: string) -> (string, string):
    """Takes raw user input and starts processing by taking the first two characters
    as dealer and the tail as raw PBN.
    Does some preliminary sanity checks.
    :rtype: tuple
    :param raw_input:
    :return: """
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
