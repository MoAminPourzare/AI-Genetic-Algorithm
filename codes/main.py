from select import select
from symbol import dotted_as_name
import turtle
import math
import random
import time
from time import sleep
from sys import argv

class Sim:
    # Set true for graphical interface
    GUI = True
    screen = None
    dots = []
    prune = False
    selection = []
    turn = ''
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)

    def _swap_turn(self, turnCur):
        if (turnCur == 'red'):
            return 'blue'
        else:
            return 'red'

    def enemy(self):
        return random.choice(self.available_moves)

    def gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'

        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0

    def gameover2(self, r, b):
        if (len(r) < len(b)):
            if len(r) < 3:
                return 0
            r.sort()
            for i in range(len(r) - 2):
                for j in range(i + 1, len(r) - 1):
                    for k in range(j + 1, len(r)):
                        if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                            return 'blue'

            if len(b) < 3: return 0
            b.sort()
            for i in range(len(b) - 2):
                for j in range(i + 1, len(b) - 1):
                    for k in range(j + 1, len(b)):
                        if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                            return 'red'
        else :
            if len(b) < 3:
                return 0
            b.sort()
            for i in range(len(b) - 2):
                for j in range(i + 1, len(b) - 1):
                    for k in range(j + 1, len(b)):
                        if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                            return 'red'

            if len(r) < 3:
                return 0
            r.sort()
            for i in range(len(r) - 2):
                for j in range(i + 1, len(r) - 1):
                    for k in range(j + 1, len(r)):
                        if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                            return 'blue'
        return 0

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def play(self, numOfNodes):
        self.initialize()
        while True:
            if self.turn == 'red':
                selection = self.mostScoreMove(depth=self.minimax_depth, player_turn=self.turn, numOfNodes=numOfNodes)
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])

            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")

            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)
            if (selection in self.available_moves):
                self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def mostScoreMove(self, depth, player_turn, numOfNodes):
        highestScore = -100000
        selectedMove = (-1, -1)
        for move in self.available_moves:
            remainingMoves = []
            remainingMoves.extend(self.available_moves)

            movesRed = []
            movesBlue = []
            movesRed.extend(self.red)
            movesBlue.extend(self.blue)

            movesRed.append(move)
            maxTurn = False
            remainingMoves.remove(move)
            numOfNodes[0] = numOfNodes[0] + 1
            moveScore = self.minimax(1, depth, maxTurn, movesRed, movesBlue, remainingMoves, -5000, 5000, numOfNodes)
            if (moveScore > highestScore):
                highestScore = moveScore
                selectedMove = move
        return selectedMove

    def minimax(self, curDepth, targetDepth, maxTurn, movesRed, movesBlue, remainingMoves, alpha, beta, numOfNodes):
        if (curDepth == targetDepth):
            score = self._evaluate(movesRed, movesBlue)
            return score

        if (maxTurn == True):
            highestScore = -100000
            for move in remainingMoves:
                _movesRed_ = []
                _movesRed_.extend(movesRed)
                _movesRed_.append(move)
                _remainingMoves_ = []
                _remainingMoves_.extend(remainingMoves)
                _remainingMoves_.remove(move)
                numOfNodes[0] = numOfNodes[0] + 1
                highestScore = max(highestScore, self.minimax(curDepth + 1, targetDepth, False, _movesRed_, movesBlue, _remainingMoves_, alpha, beta, numOfNodes))
                if (self.prune == True):
                    alpha = max(alpha, highestScore)
                    if beta <= alpha:
                        break
            return highestScore

        else:
            lowestScore = 100000
            for move in remainingMoves:
                _movesBlue_ = []
                _movesBlue_.extend(movesBlue)
                _movesBlue_.append(move)
                _remainingMoves_ = []
                _remainingMoves_.extend(remainingMoves)
                _remainingMoves_.remove(move)
                numOfNodes[0] = numOfNodes[0] + 1
                lowestScore = min(lowestScore, self.minimax(curDepth + 1, targetDepth, True, movesRed, _movesBlue_, _remainingMoves_, alpha, beta, numOfNodes))
                if (self.prune == True):
                    beta = min(beta, lowestScore)
                    if beta <= alpha:
                        break
            return lowestScore

    def _evaluate(self, movesRed, movesBlue):
        score = 0
        if (self.gameover2(movesRed, movesBlue) == 'red'):
            score += 1000
        elif (self.gameover2(movesRed, movesBlue) == 'blue'):
            score -= 1000
        else:
            twoAdjacentSides_E_R = self.calcTwoAdjacentSides_E(movesRed, movesBlue)
            twoAdjacentSides_E_B = self.calcTwoAdjacentSides_E(movesBlue, movesRed)

            twoAdjacentSides_R = self.calcTwoAdjacentSides(movesRed, movesBlue)
            twoAdjacentSides_B = self.calcTwoAdjacentSides(movesBlue, movesRed)

            for i in range(twoAdjacentSides_E_R):
                score -= 50
            for i in range(twoAdjacentSides_E_B):
                score += 50
            for i in range(twoAdjacentSides_R):
                score += 20
            for i in range(twoAdjacentSides_B):
                score -= 20

        return score

    def calcTwoAdjacentSides_E(self, mainMoves, minorMoves):
        counter = 0
        for i in range(0, len(mainMoves) - 1):
            for j in range(i + 1, len(mainMoves)):
                if ((mainMoves[i][0] == mainMoves[j][0] and mainMoves[i][1] != mainMoves[j][1] and (((mainMoves[i][1], mainMoves[j][1]) not in minorMoves) and ((mainMoves[j][1], mainMoves[i][1]) not in minorMoves)))
                or (mainMoves[i][1] == mainMoves[j][1] and mainMoves[i][0] != mainMoves[j][0] and (((mainMoves[i][0], mainMoves[j][0]) not in minorMoves) and ((mainMoves[j][0], mainMoves[i][0]) not in minorMoves)))
                or (mainMoves[i][0] == mainMoves[j][1] and mainMoves[i][1] != mainMoves[j][0] and (((mainMoves[i][1], mainMoves[j][0]) not in minorMoves) and ((mainMoves[j][0], mainMoves[i][1]) not in minorMoves)))
                or (mainMoves[i][1] == mainMoves[j][0] and mainMoves[i][0] != mainMoves[j][1] and (((mainMoves[i][0], mainMoves[j][1]) not in minorMoves) and ((mainMoves[j][1], mainMoves[i][0]) not in minorMoves)))):
                    counter = counter + 1
        return counter

    def calcTwoAdjacentSides(self, mainMoves, minorMoves):
        counter = 0
        for i in range(0, len(mainMoves) - 1):
            for j in range(i + 1, len(mainMoves)):
                if ((mainMoves[i][0] == mainMoves[j][0] and mainMoves[i][1] != mainMoves[j][1] and (((mainMoves[i][1], mainMoves[j][1]) in minorMoves) or ((mainMoves[j][1], mainMoves[i][1]) in minorMoves)))
                or (mainMoves[i][1] == mainMoves[j][1] and mainMoves[i][0] != mainMoves[j][0] and (((mainMoves[i][0], mainMoves[j][0]) in minorMoves) or ((mainMoves[j][0], mainMoves[i][0]) in minorMoves)))
                or (mainMoves[i][0] == mainMoves[j][1] and mainMoves[i][1] != mainMoves[j][0] and (((mainMoves[i][1], mainMoves[j][0]) in minorMoves) or ((mainMoves[j][0], mainMoves[i][1]) in minorMoves)))
                or (mainMoves[i][1] == mainMoves[j][0] and mainMoves[i][0] != mainMoves[j][1] and (((mainMoves[i][0], mainMoves[j][1]) in minorMoves) or ((mainMoves[j][1], mainMoves[i][0]) in minorMoves)))):
                    counter = counter + 1
        return counter

if __name__=="__main__":
    start = time.time()
    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    numOfNodes = [0]
    results = {"red": 0, "blue": 0}
    for i in range(100):
        print(i)
        results[game.play(numOfNodes)] += 1
        
    print(results)
    end = time.time()
    print("time execution :", (end-start) * 10**3, "ms")
    print("number of seen nodes : ", numOfNodes[0])
