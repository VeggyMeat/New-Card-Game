from random import randint


# some code to shuffle a deck of cards
def shuffle(deck):
    newDeck = []
    while len(deck) > 0:
        card = deck[randint(0, len(deck)-1)]
        newDeck.append(card)
        deck.remove(card)
    return newDeck


# draws a card from the deck places it randomly on the board and removes it from the stack
def drawCard(board, stackCards):
    shuffle(stackCards)
    while True:
        if not board[randint(0, 4)][randint(0, 4)]['card']:
            board[randint(0, 4)][randint(0, 4)]['card'] = stackCards[0]
            stackCards.pop(0)
            break
    return board, stackCards
