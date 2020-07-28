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
    stackCards = shuffle(stackCards)
    while True:
        cords = (randint(0, 4), randint(0, 4))
        if not board[cords[0]][cords[1]]['card']:
            try:
                board[cords[0]][cords[1]]['card'] = stackCards[0]
                board[cords[0]][cords[1]]['card'].x, board[cords[0]][cords[1]]['card'].y, board[cords[0]][cords[1]]['card'].screenX, board[cords[0]][cords[1]]['card'].screenY = cords[0], cords[1], cords[0] * 120 + 50, cords[1] * 170 + 50
                stackCards.pop(0)
                break
            except IndexError as e:
                print(e)
                break
    return board, stackCards
