"""Tests for the card value objects and the deck (FR-02)."""

from dataclasses import FrozenInstanceError
from random import Random

import pytest

from italian_card_games.engine.cards import Card, Deck, DeckFactory, Rank, Suit


class TestSuit:
    def test_has_the_four_italian_suits(self):
        assert {suit.name for suit in Suit} == {"DENARI", "COPPE", "SPADE", "BASTONI"}


class TestRank:
    @pytest.mark.parametrize("value", range(1, 11))
    def test_accepts_values_from_1_to_10(self, value):
        assert Rank(value).value == value

    @pytest.mark.parametrize("value", [-1, 0, 11, 100])
    def test_rejects_values_outside_1_to_10(self, value):
        with pytest.raises(ValueError):
            Rank(value)

    def test_is_equal_by_value(self):
        assert Rank(3) == Rank(3)
        assert Rank(3) != Rank(4)
        assert hash(Rank(3)) == hash(Rank(3))


class TestCard:
    def test_is_equal_by_value(self):
        assert Card(Suit.SPADE, Rank(8)) == Card(Suit.SPADE, Rank(8))
        assert Card(Suit.SPADE, Rank(8)) != Card(Suit.COPPE, Rank(8))
        assert Card(Suit.SPADE, Rank(8)) != Card(Suit.SPADE, Rank(7))

    def test_can_be_used_in_sets(self):
        cards = {Card(Suit.SPADE, Rank(8)), Card(Suit.SPADE, Rank(8))}
        assert len(cards) == 1

    def test_is_immutable(self):
        card = Card(Suit.SPADE, Rank(8))
        with pytest.raises(FrozenInstanceError):
            card.suit = Suit.COPPE  # type: ignore[misc]

    def test_has_a_readable_string_form(self):
        assert str(Card(Suit.SPADE, Rank(8))) == "8 of SPADE"


class TestDeck:
    def test_has_40_distinct_cards(self):
        deck = DeckFactory.ordered()
        assert len(deck) == 40
        assert len(set(deck.cards)) == 40

    def test_has_every_rank_of_every_suit(self):
        deck = DeckFactory.ordered()
        expected = {Card(suit, Rank(value)) for suit in Suit for value in range(1, 11)}
        assert set(deck.cards) == expected

    def test_rejects_the_wrong_number_of_cards(self):
        with pytest.raises(ValueError):
            Deck(DeckFactory.ordered().cards[:-1])

    def test_rejects_duplicate_cards(self):
        cards = DeckFactory.ordered().cards
        with pytest.raises(ValueError):
            Deck((cards[0],) + cards[:-1])


class TestDeckFactory:
    def test_ordered_deck_is_always_the_same(self):
        assert DeckFactory.ordered() == DeckFactory.ordered()

    def test_shuffled_deck_has_the_same_cards_as_the_ordered_one(self):
        shuffled = DeckFactory.shuffled(Random(1))
        assert set(shuffled.cards) == set(DeckFactory.ordered().cards)

    def test_same_seed_gives_the_same_order(self):
        assert DeckFactory.shuffled(Random(42)) == DeckFactory.shuffled(Random(42))

    def test_different_seeds_give_different_orders(self):
        assert DeckFactory.shuffled(Random(1)) != DeckFactory.shuffled(Random(2))

    def test_shuffling_changes_the_order(self):
        assert DeckFactory.shuffled(Random(1)) != DeckFactory.ordered()

    def test_shuffling_does_not_modify_other_decks(self):
        ordered = DeckFactory.ordered()
        DeckFactory.shuffled(Random(1))
        assert ordered == DeckFactory.ordered()
