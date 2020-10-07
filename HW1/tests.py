import unittest

from tic_tac import TicTac, BadInput


class TestTicTac(unittest.TestCase):

    def setUp(self):
        self.game = TicTac()

    def test_validate_input(self):
        with self.assertRaises(BadInput):
            self.game.validate_input('a')

        with self.assertRaises(BadInput):
            self.game.validate_input(70)

        with self.assertRaises(BadInput):
            self.game.validate_input(-7)

        self.game.make_move(3)
        with self.assertRaises(BadInput):
            self.game.validate_input(3)

        self.assertEqual(self.game.validate_input(4), 4)

    def test_make_move(self):
        self.assertEqual(self.game.board[3], 0)
        self.game.make_move(3)
        self.assertEqual(self.game.board[3], 1)

    def test_change_turn(self):
        self.assertEqual(self.game.change_turn(), 2)
        self.assertEqual(self.game.change_turn(), 1)
        self.assertEqual(self.game.change_turn(), 2)

    def test_check_end(self):
        self.assertFalse(self.game.check_end())
        self.game.make_move(0)
        self.game.make_move(1)
        self.game.make_move(2)
        self.assertTrue(self.game.check_end())


if __name__ == '__main__':
    unittest.main()
