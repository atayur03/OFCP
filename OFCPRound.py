import Hand5
import Hand3
from collections import defaultdict

class Round:
  def __init__(self, player_names:list):
    self.player_names = player_names
    self.num_players = len(player_names)
    self.str_hands = []
    for name in player_names:
      self.str_hands.append(self.parse(name))
    self.score = self.score()

  def parse(self, name:str):
    '''
    input: player name
    returns: (name, top, middle, bottom, royalties)
    '''

    top = input(f"Please top three card hand for {name}: ")
    if top == 'foul':
      return (name, "foul", "foul", "foul", 0)
    royalties = 0
    input_valid_top = Hand5.PokerHand.is_valid_hand3(top)
    while not input_valid_top:
      top = input(f"Invalid Entry. Please top three card hand for {name}: ")
      input_valid_top = Hand5.PokerHand.is_valid_hand3(top)
    royalties += Hand3.calc_royalties(Hand3.rank(Hand3.inputTo3(top)))

    middle = input(f"Please middle 5 card hand for {name}: ")
    input_valid_middle = Hand5.PokerHand.is_valid_hand5(middle)
    while not input_valid_middle:
      middle = input(f"Invalid Entry. Please middle 5 card hand for {name}: ")
      input_valid_middle = Hand5.PokerHand.is_valid_hand5(middle)
    royalties += Hand5.PokerHand(middle).calculate_royalties_middle()

    bottom = input(f"Please bottom 5 card hand for {name}: ")
    input_valid_bottom = Hand5.PokerHand.is_valid_hand5(bottom)
    while not input_valid_bottom:
      bottom = input(f"Invalid Entry. Please bottom 5 card hand for {name}: ")
      input_valid_bottom = Hand5.PokerHand.is_valid_hand5(bottom)
    royalties += Hand5.PokerHand(bottom).calculate_royalties_bottom()
    
    return (name, top, middle, bottom, royalties)
  

  def score(self):
    hands = self.str_hands
    num_players = len(hands)
    top = defaultdict()
    mid = defaultdict()
    bottom = defaultdict()
    royalties = defaultdict()
    scores = defaultdict()
    names = self.player_names
    sum_royalties = 0
    for n, t, m, b, r in hands:
      sum_royalties += r
      top[n] = t
      mid[n] = m
      bottom[n] = b
      royalties[n] = r

    for n1 in names:
      scores[n1] = (royalties[n1] * num_players) - sum_royalties
      for n2 in names:
        if n1 != n2:
          top_win = Hand3.firstBetter3(top[n1], top[n2])
          mid_win = Hand5.PokerHand.firstBetter5(mid[n1], mid[n2])
          bottom_win = Hand5.PokerHand.firstBetter5(bottom[n1], bottom[n2])
          net = top_win + mid_win + bottom_win
          scores[n1] += net
          if net == 3:
            scores[n1] += 3
          if net == -3:
            scores[n1] -= 3
    
    res = []
    for name in names:
      res.append((name, scores[name]))
    return res

if __name__ == "__main__":
  r = Round(["Ashwin", "Ashwin2", "Ashwin3", "Ashwin4"])
  print(r.score)
           



    

    




