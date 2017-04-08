from shatter.solver import solve


@solve()
def is_alive(alive, neighbors):
    pass


@solve()
def valid_indexes(idx1, idx2, max_idx1, max_idx2):
    pass


@solve()
def me(x, y, idx, idy):
    pass


def get_neighbors(x, y, cells):

    n = []
    l_y = len(cells)
    l_x = len(cells[0])

    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if valid_indexes(i, j, l_x, l_y) and not me(x, y, i, j):
                n.append(cells[j][i])

    return n


def solve(cells):

    new_cells = [[[] for i in range(len(cells[0]))] for i in range(len(cells))]

    for j in range(0, len(cells)):
        for i in range(0, len(cells[0])):
            n = get_neighbors(i, j, cells)
            new_cells[j][i] = is_alive(cells[j][i], n)

    return new_cells

