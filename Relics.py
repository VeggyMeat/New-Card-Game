from random import randint
from Cards import *
from Classes import Card
from Definitions import *
relics = {}

# relics


def Blank(self, board, player, enemies):
    return board, player, enemies


def MechaniseRelic(self, board, player, enemies, tag, relics):
    attackedSquares = []
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            if card:
                tempAttack = 0
                for index in card['attacked']:
                    tempAttack += card['attacked'][index]
                if tempAttack > 0:
                    attackedSquares.append((counter1, counter2))
                counter2 += 1
        counter1 += 1
    if len(attackedSquares) > 0:
        cords = attackedSquares[randint(0, len(attackedSquares) - 1)]
        board[cords[0]][cords[1]]['block'] = player.hp
    player.maxHP -= 1
    return board, player, enemies


relics['mechanise relic'] = [MechaniseRelic, Blank, ['endTurn'], False, 'mechanise relic', 'Apply armour equal to your health at a random attacked square and lose 1 max HP at the end of each turn.']


def Demonfire(self, board, player, enemies, tag, relics):
    for enemy in enemies:
        enemy.hit(25, player)
    return board, player, enemies


relics['demonfire'] = [Demonfire, Blank, ['endTurn'], False, 'demon fire', 'reduces enemies health by 25 every turn']


def RitualStone(self, board, player, enemies, tag, relics):
    for x in range(5):
        card = cards['demonic seal']
        player.stackCards.append(Card(0, 0, 0, 0, card[0], card[1], card[2], card[3], card[4], card[5], card[6]))
    player.stackCards = shuffle(player.stackCards)
    return board, player, enemies


relics['ritual stone'] = [RitualStone, Blank, ['startEncounter'], True, 'ritual stone', 'adds 5 demonic seals at the start of each encounter']


def TwigOfTheWorldTree(self, board, player, enemies):
    player.healingMultiplyer = 1.5
    return board, player, enemies


relics['twig of the world tree'] = [Blank, TwigOfTheWorldTree, [], True, 'twig of the world tree', 'All healing increased by 50%']


def ShardOfGalanor(self, board, player, enemies):
    player.boltDamage += 5
    return board, player, enemies


relics['shard of galanor'] = [Blank, ShardOfGalanor, [], True, 'shard of galanor', 'Bolts deal 5 more damage']


def SerratedShield(self, board, player, enemies, tag, relics):
    for row in board:
        for card in row:
            card['block'] *= 2
    return board, player, enemies


relics['serrated shield'] = [SerratedShield, Blank, ['endTurn'], True, 'serrated shield', 'doubles block at the end of the turn']


def SupplyBag(self, board, player, enemies, tag, relics):
    for x in range(2):
        board, player.stackCards = drawCard(board, player.stackCards)
    return board, player, enemies


relics['supply bag'] = [SupplyBag, Blank, ['startEncounter'], True, 'supply bag', 'draw two extra cards on your first turn of each encounter']


def WitchDoctorsSyringe(self, board, player, enemies):
    player.poisonMultiplier = 2
    return board, player, enemies


relics['witch doctors syringe'] = [Blank, WitchDoctorsSyringe, [], True, 'which doctors syringe', 'apply all poison twice']


def WitchDoctorsHerbs(self, board, player, enemies, tag, relics):
    if player.poison > 0:
        player.hit(player.poison)
        player.poison = int(player.poison / 2)

    for enemy in enemies:
        if enemy.poison > 0:
            enemy.hit(enemy.poison, player)
            enemy.poison -= int(enemy.poison / 2)

    return board, player, enemies


relics['witch doctors herbs'] = [WitchDoctorsHerbs, Blank, ['endTurn'], True, 'which doctors herbs', 'deal full poison damage but half stacks per turn']


def DefenciveStanceRelic(self, board, player, enemies, tag, relics):
    blockCards = []
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            if card['block'] > 0:
                blockCards.append([counter1, counter2, card['block']])
            counter2 += 1
        counter1 += 1

    total = 10
    while total != 0:
        random = blockCards[randint(0, len(blockCards) - 1)]
        board[random[0]][random[1]]['block'] -= 1
        random[2] -= 1
        if board[random[0]][random[1]]['block'] == 0:
            blockCards.remove(random)

    return board, player, enemies


relics['defencive stance relic'] = [DefenciveStanceRelic, Blank, ['endTurn'], False, 'defencive stance relic', 'Only lose 10 block at the end of your turn.']


def BurningHeart(self, board, player, enemies, tag, relics):
    board, player.stackCards = drawCard(board, player.stackCards)
    player.hp -= 1

    return board, player, enemies


relics['burning heart'] = [BurningHeart, Blank, ['startTurn'], True, 'burning heart', 'Take 1 damage at the beginning of every turn. Draw 1 extra card per turn']
