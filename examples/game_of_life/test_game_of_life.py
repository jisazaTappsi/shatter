import unittest

# TODO: check imports fucks!
from shatter.solver import Rules, Code
from examples.game_of_life.game_of_life import is_alive, valid_indexes, get_neighbors, me, solve


class GameOfLifeTest(unittest.TestCase):

    def test_living_rule(self):

        """
        1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        2. Any live cell with more than three live neighbours dies, as if by overcrowding.
        3. Any live cell with two or three live neighbours lives on to the next generation.
        4. Any dead cell with exactly three live neighbours becomes a live cell.
        """

        r = Rules(rule1=Code(code_str='sum(neighbors) < 2'), output=False)
        r.add(rule2=Code('sum(neighbors) > 3'), output=False)
        r.add(alive=True, rule3=Code(code_str='sum(neighbors) == 2'), output=True)
        r.add(alive=True, rule4=Code(code_str='sum(neighbors) == 3'), output=True)
        r.add(alive=False, rule5=Code(code_str='sum(neighbors) == 3'), output=True)

        r.solve(is_alive, self)

    def test_valid_indexes(self):

        idx1 = Code()
        idx2 = Code()
        max_idx1 = Code()
        max_idx2 = Code()

        # TODO: ERROR when output is not present. FIX
        r = Rules(more_than1=idx1 >= 0,
                     less_than1=idx1 < max_idx1,
                     more_than2=idx2 >= 0,
                     less_than2=idx2 < max_idx2, output=True)

        r.solve(valid_indexes, self)

    def test_me(self):

        #TODO: make it right should return not (idx1 != x and idx1 != y)
        #r = Rules(different1=Code('idx1 != x'),
        #          different2=Code('idx2 != y'), output=False)

        idx = Code()
        idy = Code()
        x = Code()
        y = Code()

        r = Rules(different1=idx == x,
                     different2=idy == y, output=True)
        r.solve(me, self)

    def test_get_neighbors(self):

        cells = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        self.assertEqual(get_neighbors(x=1, y=1, cells=cells), [0, 1, 0, 0, 0, 0, 1, 0])
        self.assertEqual(get_neighbors(x=0, y=0, cells=cells), [1, 0, 1])
        self.assertEqual(get_neighbors(x=1, y=0, cells=cells), [0, 0, 0, 1, 0])
        self.assertEqual(get_neighbors(x=2, y=1, cells=cells), [1, 0, 1, 1, 0])

    def test_solve(self):

        cells = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[0, 0, 0], [0, 0, 0], [0, 1, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[1, 1, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[1, 1, 0], [1, 0, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[1, 1, 0], [1, 1, 0], [0, 0, 0]])

        # Square lives forever!!!
        cells = [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[1, 1, 0], [1, 1, 0], [0, 0, 0]])