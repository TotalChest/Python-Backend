import numpy as np


class BadInput(Exception):
    pass


class TicTac:
    win_mask = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 1, 1, 0, 0, 0],
                         [1, 1, 1, 0, 0, 0, 1, 1, 1],
                         [1, 0, 0, 1, 0, 0, 1, 0, 0],
                         [0, 1, 0, 0, 1, 0, 0, 1, 0],
                         [0, 0, 1, 0, 0, 1, 0, 0, 1],
                         [1, 0, 0, 0, 1, 0, 0, 0, 1],
                         [0, 0, 1, 0, 1, 0, 1, 0, 0]])
    print_mapping = {1: 'x', 5: 'o', 0: ' '}

    def __init__(self):
        """
        Init the board and set prayer`s turn

        turn = 1 for first player
        turn = 2 for second player
        """
        self.board = [0] * 9
        self.turn = 1

    def show_board(self):
        """Print the board in console"""
        for i in range(3):
            print(TicTac.print_mapping[self.board[3*i]],
                  TicTac.print_mapping[self.board[3*i + 1]],
                  TicTac.print_mapping[self.board[3*i + 2]],)

    def validate_input(self, move):
        """Check input"""
        try:
            move = int(move)
        except ValueError:
            print('Bad input: not integer.')
            raise BadInput from ValueError

        if move > 8 or move < 0:
            print('Bad input: out of bounds.')
            raise BadInput

        if self.board[move] != 0:
            print('Bad input: cell is not empty.')
            raise BadInput

        return int(move)

    def make_move(self, move):
        """Change board state"""
        # 5 for fast winner cheking
        self.board[move] = 1 if self.turn == 1 else 5

    def change_turn(self):
        self.turn = 2 if self.turn == 1 else 1
        return self.turn

    def start_game(self):
        """Main game loop"""
        end = False
        step = 0

        while not end and step < 9:
            self.show_board()
            step += 1
            bad_input = True
            while bad_input:
                move = input(f'Player {self.turn}: ')
                try:
                    move = self.validate_input(move)
                except BadInput:
                    print('Try again.')
                else:
                    bad_input = False
            self.make_move(move)
            self.change_turn()
            end = self.check_end()

        self.show_board()
        if end:
            print(f'Player {self.change_turn()} win!')
        else:
            print('It is draw!')

    def check_end(self):
        """If 3 items under mask is the same then True"""
        state = np.dot(TicTac.win_mask, np.array(self.board))
        return (3 in state) or (15 in state)


if __name__ == '__main__':
    game = TicTac()
    game.start_game()
