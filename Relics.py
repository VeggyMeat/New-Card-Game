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


def BraceRelic(self, board, player, enemies, tag, relics):
    board[randint(0, 4)][randint(0, 4)]['block'] += 5
    return board, player, enemies


relics['brace relic'] = [BraceRelic, Blank, ['takeDamage'], False, 'brace relic', 'Every time you take hp damage apply block 5 to a random grid space.']


def EnragedRelic(self, board, player, enemies, tag, relics):
    player.nextMana += 1
    return board, player, enemies


relics['enraged relic'] = [EnragedRelic, Blank, ['enemyDamage'], False, 'enraged relic', 'Gain 1 energy every time you take unblocked attack damage']


def CrookedStealthCrossbow(self, board, player, enemies, tag, relics):
    targets = {'enemies': enemies}
    none = False
    none, targets, board, player = player.fires['bolt'][0](self, targets, board, none, none, none, none, player)
    return board, player, enemies


relics['crooked stealth crossbow'] = [CrookedStealthCrossbow, Blank, ['cardDiscarded'], True, 'crooked stealth crossbow', 'Fire one bolt every time a card is discarded']


def DyingEmbers(self, board, player, enemies, tag, relics):
    player.hp += 1
    return board, player, enemies


relics['dying embers'] = [DyingEmbers, Blank, ['takeDamage'], True, 'dying embers', 'Lose one less health every time you would take hp damage']


def InnerPeace(self, board, player, enemies, tag, relics):
    total = 0
    for card in player.deck:
        if card[-7:-1] + card[-1] == 'passive':
            total += 1
    total = int(total / 3)
    for x in range(total):
        board, player.stackCards = drawCard(board, player.stackCards)
    return board, player, enemies


relics['inner peace'] = [InnerPeace, Blank, ['startEncounter'], True, 'inner peace', 'Draw an extra card on your first turn of combat for the first turn of combat for every 3 power cards in your deck']


def Recycle(self, board, player, enemies, tag, relics):
    board, player.stackCards = drawCard(board, player.stackCards)
    return board, player, enemies


def RecycleStart(self, board, player, enemies):
    player.relics.pop(randint(0, len(player.relics) - 1))
    return board, player, enemies


relics['recycle'] = [Recycle, RecycleStart, ['startTurn'], True, 'recycle', 'Draw an extra card every turn. Lose a random relic.']
