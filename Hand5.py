from collections import Counter

RANKS = "23456789TJQKA"
SUITS = "cdhs"

OFC_ROYALTIES = {
    "Straight": 2,
    "Flush": 4,
    "Full House": 6,
    "Four of a Kind": 10,
    "Straight Flush": 15,
    "Royal Flush": 25
}

class PokerHand:
    def __init__(self, hand_str: str):
        if not self.is_valid_hand5(hand_str):
            raise ValueError("Invalid hand input. Must be 5 unique cards.")
        self.hand_str = hand_str
        self.cards = self.parse_hand()

    @staticmethod
    def is_valid_hand5(hand_str: str):
        """Verifies if the input string represents a valid 5-card poker hand."""
        if len(hand_str) != 10:
            return False
        
        parsed_cards = [hand_str[i:i+2] for i in range(0, len(hand_str), 2)]
        if len(parsed_cards) != 5:
            return False
        
        for card in parsed_cards:
            if card[0] not in RANKS or card[1] not in SUITS:
                return False
        return True

    @staticmethod
    def is_valid_hand3(hand_str: str):
        """Verifies if the input string represents a valid 5-card poker hand."""
        if len(hand_str) != 6:
            return False
        
        parsed_cards = [hand_str[i:i+2] for i in range(0, len(hand_str), 2)]
        if len(parsed_cards) != 3:
            return False
        
        for card in parsed_cards:
            if card[0] not in RANKS or card[1] not in SUITS:
                return False
        return True

    def calculate_royalties_bottom(self):
        """Calculates royalties based on Open Face Chinese scoring."""
        rank_value, _ = self.get_hand_rank()
        
        if rank_value == 8:
            return OFC_ROYALTIES["Straight Flush"] if max(_) < 14 else OFC_ROYALTIES["Royal Flush"]
        elif rank_value == 7:
            return OFC_ROYALTIES["Four of a Kind"]
        elif rank_value == 6:
            return OFC_ROYALTIES["Full House"]
        elif rank_value == 5:
            return OFC_ROYALTIES["Flush"]
        elif rank_value == 4:
            return OFC_ROYALTIES["Straight"]
        else:
            return 0
    
    def calculate_royalties_middle(self):
        rank_value, _ = self.get_hand_rank()
        if rank_value == 3:
            return 2
        else:
            return 2 * self.calculate_royalties_bottom()

    def parse_hand(self):
        """Parses the hand string into a list of (rank, suit) tuples."""
        return [(self.hand_str[i], self.hand_str[i+1]) for i in range(0, len(self.hand_str), 2)]

    def get_hand_rank(self):
        """Determines the rank of the hand based on poker hand rankings."""
        ranks = sorted([RANKS.index(rank)+2 for rank, suit in self.cards], reverse=True)
        suits = [suit for rank, suit in self.cards]
        rank_counts = Counter(ranks)
        count_values = sorted(rank_counts.values(), reverse=True)
        
        is_flush = len(set(suits)) == 1
        is_straight = len(rank_counts) == 5 and (max(ranks) - min(ranks) == 4)
        
        if is_straight and is_flush:
            return (8, max(ranks))  # Straight flush
        elif count_values == [4, 1] or count_values == [5]:
            return (7, ranks)  # Four of a kind
        elif count_values == [3, 2]:
            return (6, ranks)  # Full house
        elif is_flush:
            return (5, ranks)  # Flush
        elif is_straight:
            return (4, max(ranks))  # Straight
        elif count_values == [3, 1, 1]:
            return (3, ranks)  # Three of a kind
        elif count_values == [2, 2, 1]:
            return (2, ranks)  # Two pair
        elif count_values == [2, 1, 1, 1]:
            return (1, ranks)  # One pair
        else:
            return (0, ranks)  # High card

    @staticmethod
    def firstBetter5(hand1: str, hand2: str):
        """Compares two poker hands and returns the winner."""
        if hand1 == 'foul' and hand2 == 'foul':
            return 0
        if hand1 == 'foul':
            return -1
        if hand2 == 'foul':
            return 1
        h1 = PokerHand(hand1)
        h2 = PokerHand(hand2)
        
        rank1 = h1.get_hand_rank()
        rank2 = h2.get_hand_rank()
        
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        else:
            return 0

