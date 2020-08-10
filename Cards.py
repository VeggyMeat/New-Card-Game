from Relics import *
from Classes import *
from Definitions import *
from copy import deepcopy
from pathlib import Path
# sets up some variables
cards = {}
cardRoot = Path("Images/Cards/")

# cards


def LuckOfTheDice(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # sets up some variables
        newBoard = deepcopy(blankBoard)
        counter1 = 0

        # makes a order which goes from (0,0) to (4,4)
        order = []

        for x in range(5):
            for y in range(5):
                order.append((x, y))
        # copies this order and shuffles it into different sections
        blankOrder = {'card': shuffle(deepcopy(order)), 'playable': shuffle(deepcopy(order)), 'attacked': shuffle(deepcopy(order)), 'spores': shuffle(deepcopy(order)), 'block': shuffle(deepcopy(order))}

        # loops through all cards
        for row in board:
            counter2 = 0
            for card in row:
                # loops through each type of the card
                for type in card:
                    # finds new places for the card's type to go based on the order for its type
                    cordsX = blankOrder[type][counter1*5+counter2][0]
                    cordsY = blankOrder[type][counter1*5+counter2][1]

                    # moves it to these ne places
                    newBoard[cordsX][cordsY][type] = card[type]

                    # checks if the type is the card class and if so resizes and adds the new co-ordinates for the card
                    if type == 'card' and newBoard[cordsX][cordsY][type] != False:
                        newBoard[cordsX][cordsY][type].x, newBoard[cordsX][cordsY][type].y, newBoard[cordsX][cordsY][type].screenX, newBoard[cordsX][cordsY][type].screenY = cordsX, cordsY, cardGapWIDTH * cordsX + cardSpaceWIDTH, cardGapHEIGHT * cordsY + cardSpaceHEIGHT
                        newBoard[cordsX][cordsY][type].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
                counter2 += 1
            counter1 += 1
        # returns saying that it was played
        return True, targets, newBoard, player
    # returns saying it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['luck of the dice'] = [LuckOfTheDice, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'luck of the dice', 'Randomize all cards positions, attacks positions and playable card position ', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def StrikeAtTheHeart(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # applies its effects to the target
        targets['enemy'][0].crippled += 2
        targets['enemy'][0].hit(15, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['strike at the heart'] = [StrikeAtTheHeart, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'strike at the heart', 'High cost, medium damage, status effect, single target', 3, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def SneakAttack(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or if its turn 1
    if board[self.x][self.y]['playable'] or turn == 1:
        # applies damage to the target
        targets['enemy'][0].hit(5, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['sneak attack'] = [SneakAttack, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'sneak attack', 'low cost, low damage, single target', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def Execute(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or the target is able to be one shot by the card
    if board[self.x][self.y]['playable'] or targets['enemy'][0].hp <= 10:
        # applies damage to the target
        targets['enemy'][0].hit(10, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['execute'] = [Execute, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'execute', 'medium cost with medium damage, single target', 2, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def IchorSurge(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or the player has no ichor left
    if board[self.x][self.y]['playable'] or player.ichorLeft == 0:
        # increases the ichor left by 1
        player.ichorLeft += 1

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['ichor surge'] = [IchorSurge, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'ichor surge', 'no cost, small ichor increase', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Fireball(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # hits the target for 20
        targets['enemy'][0].hit(20, player, False)
        # hits all the other enemies for 3
        for enemy in targets['enemies']:
            if enemy.id != targets['enemy'][0].id:
                enemy.hit(3, player)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['fireball'] = [Fireball, pygame.image.load(str(cardRoot / 'Fireball.png')), 'fireball', 'High cost, high damage to single target, low damage to other targets', 4, True, {'enemy': 1, 'card': 0, 'enemies': 1, 'spot': 0}]


def Mechanise(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(Relic(relics['mechanise relic'][0], relics['mechanise relic'][1], relics['mechanise relic'][2], relics['mechanise relic'][3], relics['mechanise relic'][4], relics['mechanise relic'][5]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['mechanise'] = [Mechanise, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'mechanise', 'Large Ichor cost, massive armour, legendary spell', 3, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def VirulentPlague(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for enemy1 in targets['enemies']:
            for enemy2 in targets['enemies']:
                enemy2.poison += 3

        for enemy in targets['enemies']:
            enemy.hp -= enemy.poison
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['virulent plague'] = [VirulentPlague, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'virulent plague', 'Medium Ichor, Large AOE, legendary spell', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def FinalStand(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # totals damage
    total = 0
    for row in board:
        for card in row:
            for id in card['attacked']:
                total += card['attacked'][str(id)]

    # checks if the card is on a playable tile or if this card prevents death
    if board[self.x][self.y]['playable'] or player.hp <= total <= player.hp + 50:
        player.totalBlock += 50
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['final stand'] = [FinalStand, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'final stand', 'small ichor cost, massive armour', 1, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def DemonicSeal(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # totals the number of demonic seals on the board
    screen = 0
    for row in board:
        for card in row:
            if card['card']:
                if card['card'].name == 'demonic seal':
                    screen += 1

    # totals the number of demonic seals in the deck
    deck = 0
    for card in player.stackCards:
        if card['card']:
            if card['card'].name == 'demonic seal':
                deck += 1

    # checks if the card is on a playable tile, there are more than one demonic seal on the board or if its the last demonic seal
    if board[self.x][self.y]['playable'] or screen > 1 or deck + screen == 1:
        # checks if its the last demonic seal and if so adds demonfire relic
        if screen + deck == 1:
            player.relics.append(Relic(relics['demonfire'][0], relics['demonfire'][1], relics['demonfire'][2], relics['demonfire'][3], relics['demonfire'][4], relics['demonfire'][5]))

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['demonic seal'] = [DemonicSeal, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'demonic seal', 'Medium cost, Does nothing until all are played', 1, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def TheWorldTree(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or if this card prevents death
    if board[self.x][self.y]['playable']:
        # adds block to the card
        board[self.x][self.y]['block'] += 15

        # goes through each card, removes its block and adds it to the player's hp
        for row in board:
            for card in row:
                player.hp += card['block']
                card['block'] = 0

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['the world tree'] = [TheWorldTree, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'the world tree', 'Large Cost, Massive Heal', 3, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def CurrencyExchange(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # totals up all the co-ordinates of where cards are
        Cards = []
        for row in board:
            for card in row:
                if card['card']:
                    Cards.append((card['card'].x, card['card'].y))

        # replaces two cards with two random cards
        for x in range(2):
            card = Cards[randint(0, len(Cards) - 1)]
            board[card[0]][card[1]]['card'] = cards[player.allCards[randint(0, len(cards) - 1)]]
        player.discard = True

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['currency exchange'] = [CurrencyExchange, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'currency exchange', 'Discards two random cards from the board. Generate two random cards.', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def LeBureauDeChange(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for x in range(3):
            board, player.stackCards = drawCard(board, player.stackCards)
        player.discard = True

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['le bureau de change'] = [LeBureauDeChange, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'le bureau de change', 'Draw 3 cards. Discard 3 cards from the board.', 0, True, {'enemy': 0, 'card': 3, 'enemies': 0, 'spot': 0}]


def Bank(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        PLAYABLE = []
        counter1 = 0
        for row in board:
            counter2 = 0
            for card in row:
                if card['card']:
                    player.gold += 3
                    player.stackCards.append(card['card'])
                    card['card'] = False
                if card['playable']:
                    PLAYABLE.append((counter1, counter2))
                counter2 += 1
            counter1 += 1
        player.discard = True
        player.stackCards = shuffle(player.stackCards)
        card = PLAYABLE[randint(0, len(PLAYABLE) - 1)]
        board[card[0]][card[1]]['card'] = player.stackCards[0]

        player.stackCards.pop(0)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['bank'] = [Bank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'bank', 'Discard all of the cards on the grid. Gain 3 currency (non-meta) per card that you discard. Draw 1 card and place it on a random active space which is empty.', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Gamble(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # sets up some variables
        available = []
        attacked = []
        counter1 = 0
        blank = {}

        # gets a blank template for a non-attacking spot
        for id in board[0][0]:
            blank[id] = 0

        # loops through each card with counters
        for row in board:
            counter2 = 0
            for card in row:
                # if theres a card in the spot then add it to the deck and remove from board
                if card['card']:
                    player.stackCards.append(card['card'])
                    card['card'] = False

                # adds to available if the card is not on an active spot
                if not card['playable']:
                    available.append((counter1, counter2))

                # adds to the attacked square list if the card does not equal the blank template
                if board[counter1][counter2]['attacked'] == blank:
                    attacked.append((counter1, counter2))
                counter2 += 1
            counter1 += 1
        player.discard = True

        # goes through and adds 5 cards to spots that aren't active
        total = 0
        for x in range(5):
            card = available[randint(0, len(available) - 1)]
            board[card[0]][card[1]]['card'] = player.stackCards[0]
            player.stackCards.pop(0)

            # checks if the spot is attacked if so increasing total count
            if board[card[0]][card[1]]['attacked'] != blank:
                total += 1

        # for how many spots where attacked it adds 5 block to a random attacked square
        for x in range(total):
            spot = available[randint(0, len(available) - 1)]
            board[spot[0]][spot[1]]['block'] += 5
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['gamble'] = [Gamble, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'gamble', 'Discard all cards on the grid. Draw 5 cards and place them on a random non-active space. Gain 5 Block on a random threatened space for each card drawn which lands on a threatened space.', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def ShieldSlam(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # totals up block
        damage = 0
        for row in board:
            for card in row:
                damage += card['block']

        # deals damage equal to that total to the enemy
        targets['enemy'][0].hit(damage, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['shield slam'] = [ShieldSlam, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'shield slam', 'low cost, deal damage equal to armour', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def ShieldStorm(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # totals up block
        damage = 0
        for row in board:
            for card in row:
                damage += card['block']
                card['block'] = 0

        # deals total damage to each enemy
        for enemy in targets['enemies']:
            enemy.hit(damage, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['shield storm'] = [ShieldStorm, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'shield storm', 'Medium cost, deal damage to all enemies with your armour', 2, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def TimeSwipe(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.ichorLeft += 2
        player.nextMana = player.maxIchor - 3
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['time swipe'] = [TimeSwipe, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'time swipe', 'Low cost, gain energy with downside', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Taunt(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # gives the card 30 block
        board[self.x][self.y]['block'] += 30

        # totals all damage from each enemy
        totalDamage = {}
        for row in board:
            for card in row:
                for id in card['attacked']:
                    totalDamage[str(id)] += card['attacked'][str(id)]

        # adds that damage
        board[self.x][self.y]['attacked'] = totalDamage
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['taunt'] = [Taunt, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'taunt', 'Low cost gain armour, all attacks target that square', 1, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def ShieldBash(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        enemyHP = targets['enemy'][0].hp
        targets['enemy'][0].hit(10, player, False)
        board[self.x][self.y]['block'] += enemyHP - targets['enemy'][0].hp
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['shield bash'] = [ShieldBash, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'shield bash', 'Medium cost, deal a bunch of damage, gain a bunch of armour', 2, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def ClumsySlash(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable'] or player.discard:
        targets['enemy'][0].hit(3, player)
        Cards = []
        for row in board:
            for card in row:
                if card['card']:
                    Cards.append((card['card'].x, card['card'].y))

        card = Cards[randint(0, len(Cards) - 1)]
        player.stackCards.append(board[card[0]][card[1]]['card'])
        board[card[0]][card[1]]['card'] = False
        player.discard = True
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['clumsy slash'] = [ClumsySlash, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'clumsy slash', 'Part of the money money bucket', 0, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def WildLeap(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        blockCards = []
        total = 0
        counter1 = 0
        for row in board:
            counter2 = 0
            for card in row:
                if card['block'] > 0:
                    card['block'] *= 3
                    total += card['block']
                    blockCards.append([counter1, counter2, card['block']])
                counter2 += 1
            counter1 += 1

        if total > 40:
            total = 40
        while total != 0:
            random = blockCards[randint(0, len(blockCards) - 1)]
            board[random[0]][random[1]]['block'] -= 1
            random[2] -= 1
            if board[random[0]][random[1]]['block'] == 0:
                blockCards.remove(random)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['wild leap'] = [WildLeap, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'wild leap', 'Part of the dodge bucket', 2, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def MicroDodge(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the target is on an attacked tile
    total = 0
    for id in targets['spot'][0][2]['attacked']:
        total += targets['spot'][0][2]['attacked'][str(id)]
    if total > 0:
        board[targets['spot'][0]][targets['spot'][1]]['block'] += 3
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['micro dodge'] = [MicroDodge, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'micro dodge', 'Part of the 0-cost bucket and the block bucket', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 1}]


def ThrowingDagger(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if not board[self.x][self.y]['playable']:
        for enemy in targets['enemies']:
            enemy.hit(3, player, False)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['throwing dagger'] = [ThrowingDagger, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'throwing dagger', 'Part of the 0-cost bucket and the multi strike damage', 0, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def DefenciveStance(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile and the target is on an attacked tile
    if board[self.x][self.y]['playable']:
        player.relics.append(Relic(relics['storm of shields relic'][0], relics['storm of shields relic'][1], relics['storm of shields relic'][2], relics['storm of shields relic'][3], relics['storm of shields relic'][4], relics['storm of shields relic'][5]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['defencive stance'] = [DefenciveStance, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'defencive stance', 'Part of the block bucket', 3, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def EnhancedDNA(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile and the target is on an attacked tile
    if board[self.x][self.y]['playable']:
        try:
            self.block
        except AttributeError:
            self.block = 1

        totalAttacked = 0
        for row in board:
            for card in row:
                for id in card['attacked']:
                    totalAttacked += card['attacked'][id]
                card['block'] += 1

        if totalAttacked == 0:
            self.block += 1
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['enhanced dna'] = [EnhancedDNA, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'enhanced dna', 'Part of the block bucket', 1, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def EvolvingParasite(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile and the target is on an attacked tile
    if board[self.x][self.y]['playable']:
        increaseDamage = False
        for enemy in targets['enemies']:
            enemy.hit(self.attack, player, True)
            if enemy.hp < 1:
                increaseDamage = True

        if increaseDamage:
            player.evolvingParasite += 2
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['evolving parasite'] = [EvolvingParasite, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'evolving parasite', 'an archetype of its own and part of the multistrike bucket', 1, True, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def Slash(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile and the target is on an attacked tile
    try:
        self.damage
    except AttributeError:
        self.damage = 7
    targets['enemy'][0].hit(self.damage, player)
    self.damage += 5
    # returns saying that it was played
    return True, targets, board, player


# appends this newly made card not in a class format so many can be made
cards['slash'] = [Slash, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'slash', 'An archetype of its own', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]
