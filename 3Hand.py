import math
import pandas as pd

mapper = {">": "A", "=": "K", "<" : "Q", ";": "J", ":": "T"}
ranks = {"set": 2, "pair": 1, "highCard": 0}

def ascii_to_card(val:int):
  if val < 50 or val > 62:
    raise Exception
  if val < 58:
    return chr(val)
  else:
    return mapper[chr(val)]

def calc_royalties(cards:tuple):
  if cards[0] == 'highCard':
    return 0
  df = pd.read_csv("3cardroyalties.csv").set_index('Unnamed: 0')
  return df[cards[0]][ascii_to_card(cards[1])]



def rank(cards:list):
  '''
  Input: 
      cards: list of three card values
  Returns:
      tuple: (rank, card, kicker)
      if high card, kicker is list of length 3
  '''
  if cards[0] == cards[1] == cards[2]:
    return ('set', cards[0], None)
  elif cards[0] == cards[1]:
    return ('pair', cards[0], cards[2])
  elif cards[1] == cards[2]:
    return  ('pair', cards[2], cards[0])
  else:
    return ('highCard', None, cards)

def inputTo3(cards:str):
  #cards = raw_input("Enter the cards (board, then 2 to 10 hands). Sample format: 5c6dTh4dJd KhQh AsJs 7h9d ...>")
  lenCards = len(cards)
  cards = cards.replace("T", ":").replace("J", ";").replace("Q", "<").replace("K", "=").replace("A", ">")
  listOfCards = (",".join(str(ord(card)) for card in cards)).split(',')
  c = [ int(item) for item in listOfCards ]
  s = sorted(zip([c[0], c[2], c[4]], [c[1], c[3], c[5]]), reverse=True)
  return [x for x, _ in s]

def firstBetter(h1:tuple, h2:tuple):
  '''
  Input:
    h1: tuple
    h2: tuple
  Returns:
    1 if h1 better
    0 if chop
    -1 if h2 better
  '''

  #check hand strength
  if ranks[h1[0]] > ranks[h2[0]]:
    return 1
  if ranks[h2[0]] > ranks[h1[0]]:
    return -1
  
  #if same strength, find better hand
  if h1[0] == 'set':
    val = int(str(ord(h1[1]))) - int(str(ord(h2[1])))
    if val == 0:
      return 0
    else:
      return math.copysign(1, val)
  if h1[0] == 'pair':
    val = int(str(ord(h1[1]))) - int(str(ord(h2[1])))
    if val == 0:
      kicker = int(str(ord(h1[2]))) - int(str(ord(h2[2])))
      if kicker == 0:
        return kicker
      else:
        return math.copysign(1, kicker)
    else:
      return math.copysign(1, val)

  if h1[0] == 'highCard':
    for i in range(3):
      if h1[2][i] > h2[2][i]:
        return 1
      if h1[2][i] < h2[2][i]:
        return -1
  return 0


      

if __name__ == "__main__":
  parse2 = rank(inputTo3("AdAdKc"))
  print(calc_royalties(parse2))

