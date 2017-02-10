import unittest

# TODO: check imports fucks!
from shatter import solver
from shatter.code import Code
from examples.bowling import start_bowling


class BowlingTest(unittest.TestCase):

    def test_is_strike(self):

        r = solver.Rules(rule=solver.Code(code_str='frame[0] == 10'), output=True)
        r.solve(start_bowling.is_strike, self)

    def test_is_spare(self):

        r = solver.Rules(rule1=solver.Code(code_str='frame[0] < 10'),
                            rule2=solver.Code(code_str='frame[0] + frame[1] == 10'),
                            output=True)
        r.solve(start_bowling.is_spare, self)

    def test_get_next_throw(self):

        i = Code()

        r = solver.Rules(before_last=(i < 9),
                            output=solver.Code(code_str='game[i+1][0]'))
        r.add(last_bonus_thow=(i == 9), output=solver.Code(code_str='game[i][2]'))
        r.solve(start_bowling.get_next_throw, self)

    def test_get_next_2_throws(self):

        i = Code()

        r = solver.Rules(last_bonus_throw=(i == 9),
                            output=solver.Code(code_str='game[i][1] + game[i][2]'))

        r.add(i == 8,
                 solver.Code(code_str='is_strike(game[i+1])'),
                 output=solver.Code(code_str='game[i+1][0] + game[i+1][1]'))

        r.add(next_is_not_strike=solver.Code(code_str='not is_strike(game[i+1])'),
                 output=solver.Code(code_str='game[i+1][0] + game[i+1][1]'))

        r.add(next_is_strike=solver.Code(code_str='is_strike(game[i+1])'),
                 output=solver.Code(code_str='game[i+1][0] + game[i+2][0]'))

        r.solve(start_bowling.get_next_2_throws, self)

    def test_get_frame_score(self):

        r = solver.Rules(not_strike=solver.Code(code_str='not is_strike(frame)'),
                            not_spare=solver.Code(code_str='not is_spare(frame)'),
                            output=solver.Code(code_str='frame[0] + frame[1]'))

        r.add(is_spare=solver.Code(code_str='is_spare(frame)'),
                 output=solver.Code(code_str='frame[0] + frame[1] + get_next_throw(i, game)'))

        r.add(is_strike=solver.Code(code_str='is_strike(frame)'),
                 output=solver.Code(code_str='frame[0] + get_next_2_throws(i, game)'))
        r.solve(start_bowling.get_frame_score, self)

    def test_recursive_get_score(self):

        r = solver.Rules(solver.Code(code_str='i == len(game)'),
                            output=0,
                            default=solver.Code(code_str='recursive_get_score(game, i + 1) + get_frame_score(game[i], game, i)'))
        r.solve(start_bowling.recursive_get_score, self)

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

