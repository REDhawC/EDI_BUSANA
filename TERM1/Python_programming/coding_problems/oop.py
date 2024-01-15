class Card:
    def __init__(self, suit, rank) -> None:
        self.suit = ["Hearts", "Diamonds", "Clubs", "Spades"][suit]
        self.rank = [
            "A",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ][rank]


c1 = Card(1, 0)
print(c1.suit, c1.rank)
