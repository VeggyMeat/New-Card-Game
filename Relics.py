from random import randint
relics = []

# relics


def MechaniseRelic(board, player, enemies):
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
    return board, player


relics.append([MechaniseRelic, ['endTurn'], False])


def Demonfire(board, player, enemies):
    for enemy in enemies:
        enemy.hp -= 25


relics.append([Demonfire, ['endTurn'], False])
