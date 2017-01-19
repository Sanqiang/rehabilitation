import random

class Game():
    def __init__(self, dims = 4):
        self.dims = dims
        self.board = [[['_' for i in range(dims)] for j in range(dims)] for k in range(dims)]

    def mark_board(self, position, player_marker = 'x'):
        # validation checking
        if len(position) != 3:
            print("posiiton is supposed to be a tuple/list of length 3")
            return 0
        for dim in range(3):
            if position[dim] >= self.dims:
                print("cannot mark outside the board")
                return 0
        if self.board[position[0]][position[1]][position[2]] is not '_':
            print("the position already marked")
            return 0
        else:
            self.board[position[0]][position[1]][position[2]] = player_marker
        winner = self.check_winner(position)
        if winner is not None:
            print("Current Winner is", winner)
            return 2
        return 1

    def check_winner(self, position):
        has_winner = True
        pre_marker = self.board[0][position[1]][position[2]]
        for i in range(1, self.dims):
            cur_marker = self.board[i][position[1]][position[2]]
            if cur_marker != pre_marker:
                has_winner = False
                break

        if has_winner:
            return pre_marker

        has_winner = True
        pre_marker = self.board[position[0]][0][position[2]]
        for i in range(1, self.dims):
            cur_marker = self.board[position[0]][i][position[2]]
            if cur_marker != pre_marker:
                has_winner = False
                break

        if has_winner:
            return pre_marker

        has_winner = True
        pre_marker = self.board[position[0]][position[1]][0]
        for i in range(1, self.dims):
            cur_marker = self.board[position[0]][position[1]][i]
            if cur_marker != pre_marker:
                has_winner = False
                break

        if has_winner:
            return pre_marker

        return None

    def visualize(self):
        print("=====Current Board=====")
        for k in range(self.dims):
            print(str(k), "th layer")
            for i in range(self.dims):
                for j in range(self.dims):
                    print(self.board[i][j][k], end= ' ')
                print("", end='\n')

    def controller(self):
        print("Game Start")
        while True:
            #player2_marker = input('Type in position of player 2 (split by white space): ')
            #player2_marker = player2_marker.strip().split(" ")
            #player2_marker = [int(ele) for ele in player2_marker]
            while True:
                player2_marker = (random.randint(0,3), random.randint(0,3), random.randint(0,3))
                result = game.mark_board(player2_marker, 'o')
                if 1 == result:
                    break
                elif 2 == result:
                    return
            game.visualize()

            while True:
                player1_marker = input('Type in position of player 1 (split by white space): ')
                player1_marker = player1_marker.strip().split(" ")
                player1_marker = [int(ele) for ele in player1_marker]
                result = game.mark_board(player1_marker, 'x')
                if 1 == result:
                    break
                elif 2 == result:
                    return
            game.visualize()


if __name__ == '__main__':
    if True:
        game = Game()
        game.controller()

    if False:
        game = Game()
        game.visualize()
        game.mark_board([1,1,1],'x')
        game.visualize()
        game.mark_board([0,0,0],'x')
        game.visualize()
        game.mark_board([1,0,0],'x')
        game.visualize()
        game.mark_board([2,0,0],'x')
        game.visualize()
        game.mark_board([3,0,0],'x')
        game.visualize()



