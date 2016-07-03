import unittest

from boolean_solver.solver import Conditions, Code, execute
from examples.bowling import start_bowling


class BowlingTest(unittest.TestCase):

    def test_is_strike(self):

        cond = Conditions(rule=Code('frame[0] == 10'), output=True)
        execute(self, start_bowling.is_strike, cond)

    def test_is_spare(self):

        cond = Conditions(rule1=Code('frame[0] < 10'),
                          rule2=Code('frame[0] + frame[1] == 10'),
                          output=True)
        execute(self, start_bowling.is_spare, cond)

    def test_get_next_throw(self):

        cond = Conditions(before_last=Code('i < 9'),
                          output=Code('game[i+1][0]'))
        cond.add(last_bonus_thow=Code('i == 9'), output=Code('game[i][2]'))
        execute(self, start_bowling.get_next_throw, cond)

    def test_get_next_2_throws(self):

        cond = Conditions(last_bonus_throw=Code('i == 9'), output=Code('game[i][1] + game[i][2]'))

        cond.add(Code('i == 8'),
                 Code('is_strike(game[i+1])'),
                 output=Code('game[i+1][0] + game[i+1][1]'))

        cond.add(next_is_not_strike=Code('not is_strike(game[i+1])'),
                 output=Code('game[i+1][0] + game[i+1][1]'))

        cond.add(next_is_strike=Code('is_strike(game[i+1])'),
                 output=Code('game[i+1][0] + game[i+2][0]'))

        execute(self, start_bowling.get_next_2_throws, cond)

    def test_get_frame_score(self):

        cond = Conditions(not_strike=Code('not is_strike(frame)'),
                          not_spare=Code('not is_spare(frame)'),
                          output=Code('frame[0] + frame[1]'))

        cond.add(is_spare=Code('is_spare(frame)'),
                 output=Code('frame[0] + frame[1] + get_next_throw(i, game)'))

        cond.add(is_strike=Code('is_strike(frame)'),
                 output=Code('frame[0] + get_next_2_throws(i, game)'))
        execute(self, start_bowling.get_frame_score, cond)

    def test_gutter_balls(self):
        game = ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0))
        self.assertEqual(start_bowling.get_score(game), 0)

    def test_all_threes(self):
        game = ((3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3))
        self.assertEqual(start_bowling.get_score(game), 60)

    def test_all_spares(self):
        game = ((4, 6), (4, 6), (4, 6), (4, 6), (4, 6), (4, 6), (4, 6), (4, 6), (4, 6), (4, 6, 4))
        self.assertEqual(start_bowling.get_score(game), 140)

    def test_nine_strikes_and_gutter(self):
        game = ((10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (0, 0))
        self.assertEqual(start_bowling.get_score(game), 240)

    def test_perfect_game(self):
        game = ((10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 10, 10))
        self.assertEqual(start_bowling.get_score(game), 300)

