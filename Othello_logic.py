class Othello:

    def __init__(self):
        self.board = []
        self.rows = 0
        self.columns = 0
        self.colnum = 0
        self.colrow = 0
        self.firstplayer = 'B'
        self.secondplayer = 'W'
        self.lines = {}
        self.turn = 0
        self.firstpoints = 0
        self.secondpoints = 0
        self.winner = None
        self.valid_moves = {}


    def firstTurn(self):
        turn = input('Who goes first? ')

        if turn == 'Black':
            self.turn = self.firstplayer
        if turn == 'White':
            self.turn = self.secondplayer


    def _new_game_board(self):

        self.rows = int(input('How many rows? '))
        self.columns = int(input('How many columns? '))

        topleft_player = input('Whose piece goes top left? ')

        if topleft_player == 'Black':
            topleft_player = self.firstplayer
            topright_player = self.secondplayer
        if topleft_player == 'White':
            topleft_player = self.secondplayer
            topright_player = self.firstplayer

        for row in range(self.rows):
            col = []
            for c in range(self.columns):
                col.append('.')
            self.board.append(col)

        col_start = int(self.columns/2) - 1
        row_start = int(self.rows/2) - 1
        self.board[row_start][col_start] = topleft_player
        self.board[row_start + 1][col_start + 1] = topleft_player
        self.board[row_start][col_start +1] = topright_player
        self.board[row_start + 1][col_start] = topright_player


    def collectMove(self):

        move = input('What move? ').split()
        self.colnum = int(move[0]) -1
        self.rownum = int(move[1]) -1


    def collectLines(self):


        self.lines = {'South':[], 'East':[], 'North':[], 'West':[], 'Northeast':[], 'Southeast':[], 'Southwest':[], 'Northwest':[]}

        for row in range(self.rownum+1, self.rows):
            self.lines['South'].append(self.board[row][self.colnum])

        for col in range(self.colnum+1, self.columns):
            self.lines['East'].append(self.board[self.rownum][col])

        for row in range(self.rownum):
            self.lines['North'].append(self.board[row][self.colnum])
        self.lines['North'].reverse()

        for col in range(self.colnum):
            self.lines['West'].append(self.board[self.rownum][col])
        self.lines['West'].reverse()

        for i in range(min(len(self.lines['North']), len(self.lines['East']))):
            self.lines['Northeast'].append(self.board[self.rownum - i - 1][self.colnum + i + 1])

        for i in range(min(len(self.lines['South']), len(self.lines['East']))):
            self.lines['Southeast'].append(self.board[self.rownum + i + 1][self.colnum + i + 1])

        for i in range(min(len(self.lines['South']), len(self.lines['West']))):
            self.lines['Southwest'].append(self.board[self.rownum + i + 1][self.colnum - i - 1])

        for i in range(min(len(self.lines['North']), len(self.lines['West']))):
            self.lines['Northwest'].append(self.board[self.rownum - i - 1][self.colnum - i - 1])


    def validateMove(self):


        self.valid_moves = {} #includes direction and index of same player's tile

        if self.board[self.rownum][self.colnum] == '.':

            for direction,player_moves in self.lines.items():
                if player_moves:
                    if player_moves[0] != '.':
                        if player_moves[0] != self.turn:
                            if self.turn in player_moves:
                                self.valid_moves[direction] = player_moves.index(self.turn)


    def makeMove(self):

        self.board[self.rownum][self.colnum] = self.turn

        for d,index in self.valid_moves.items():

            direction = d
            flip = int(index)

            for i in range(flip + 1):
                if direction == 'North':
                    self.board[self.rownum - i][self.colnum] = self.turn
                if direction == 'South':
                    self.board[self.rownum + i][self.colnum] = self.turn
                if direction == 'East':
                    self.board[self.rownum][self.colnum + i] = self.turn
                if direction == 'West':
                    self.board[self.rownum][self.colnum - i] = self.turn
                if direction == 'Northeast':
                    self.board[self.rownum - i][self.colnum + i] = self.turn
                if direction == 'Southeast':
                    self.board[self.rownum + i][self.colnum + i] = self.turn
                if direction == 'Southwest':
                    self.board[self.rownum + i][self.colnum - i] = self.turn
                if direction == 'Northwest':
                    self.board[self.rownum - i][self.colnum - i] = self.turn

    def printBoard(self):

        for row in self.board:
            print(''.join(str(cell) for cell in row))


    def printPoints(self):

        self.firstpoints = 0
        self.secondpoints = 0

        for row in self.board:
            for col in row:
                if col == self.firstplayer:
                    self.firstpoints += 1
                if col == self.secondplayer:
                    self.secondpoints += 1

        print('Black: ', self.firstpoints)
        print('White: ', self.secondpoints)


    def changeTurn(self):

        # if len(self.valid_moves) == 0:
        #     return self.turn
        # else:
        if self.turn == self.firstplayer:
            self.turn = self.secondplayer
        else:
            self.turn = self.firstplayer


    def anyMoves(self):


        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == '.':
                    self.rownum = row
                    self.colnum = col
                    self.collectLines()
                    self.validateMove()
                    if len(self.valid_moves) > 0:
                        return True

        return False


    def gameOver(self):

        if self.firstpoints > self.secondpoints:
            self.winner = 'Black'
        else:
            self.winner = 'White'

        print('Game Over')
        print('Winner: ', self.winner)


    def gameLoop(self):

        while True:
            if self.anyMoves():
                self.gameFunctions()
                self.changeTurn()
            else:
                self.changeTurn()
                if self.anyMoves():
                    self.gameLoop()
                else:
                    self.gameOver()
                    break


    def gameFunctions(self):

        self.collectMove()
        self.collectLines()
        self.validateMove()

        if len(self.valid_moves) > 0:
            self.makeMove()
            self.printBoard()
            self.printPoints()

        else:
            print ('Invalid Move')
            self.gameFunctions()


    def mainLoop(self):

        self.firstTurn()
        self._new_game_board()
        self.printBoard()
        self.gameLoop()


game = Othello()
game.mainLoop()
