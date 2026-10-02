from dataclasses import dataclass
from enum import Enum
from random import Random

MIN_RANK = 1
MAX_RANK = 10
DECK_SIZE = 40


class Suit(Enum):
    """The four suits (semi) of the Italian deck."""

    DENARI = "denari"
    COPPE = "coppe"
    SPADE = "spade"
    BASTONI = "bastoni"


@dataclass(frozen=True, slots=True)
class Rank:
    """The number on a card, from 1 (the asso) to 10."""

    value: int

    def __post_init__(self) -> None:
        if not MIN_RANK <= self.value <= MAX_RANK:
            raise ValueError(
                f"rank must be between {MIN_RANK} and {MAX_RANK}, got {self.value}"
            )


@dataclass(frozen=True, slots=True)
class Card:
    """A card of the Italian deck, identified by its suit and rank."""

    suit: Suit
    rank: Rank

    def __str__(self) -> str:
        return f"{self.rank.value} of {self.suit.name}"


@dataclass(frozen=True, slots=True)
class Deck:
    """An immutable deck of exactly 40 distinct cards, in a given order."""

    cards: tuple[Card, ...]

    def __post_init__(self) -> None:
        if len(self.cards) != DECK_SIZE:
            raise ValueError(f"a deck has {DECK_SIZE} cards, got {len(self.cards)}")
        if len(set(self.cards)) != DECK_SIZE:
            raise ValueError("a deck cannot contain duplicate cards")

    def __len__(self) -> int:
        return len(self.cards)


class DeckFactory:
    """Builds decks. Shuffling uses an injected random source, so it is reproducible."""

    @staticmethod
    def ordered() -> Deck:
        """The deck in its natural order: suit by suit, ranks 1 to 10."""
        return Deck(
            tuple(
                Card(suit, Rank(value))
                for suit in Suit
                for value in range(MIN_RANK, MAX_RANK + 1)
            )
        )

    @staticmethod
    def shuffled(rng: Random) -> Deck:
        """A new shuffled deck. The same seed always gives the same order."""
        cards = list(DeckFactory.ordered().cards)
        rng.shuffle(cards)
        return Deck(tuple(cards))
