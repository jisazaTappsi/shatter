
"""
http://code.joejag.com/coding-dojo/bowling-scores/
"""


from boolean_solver import solver as s


@s.solve()
def is_spare(frame):
    return frame[0] < 10 and frame[0] + frame[1] == 10

@s.solve()
def is_strike(frame):
    return frame[0] == 10

@s.solve()
def get_next_throw(i, game):

    if i < 9:
        return game[i+1][0]

    if i == 9:
        return game[i][2]

    return False


@s.solve()
def get_next_2_throws(i, game):

    if i == 9:
        return game[i][1] + game[i][2]

    if i == 8 and is_strike(game[i+1]) or not is_strike(game[i+1]):
        return game[i+1][0] + game[i+1][1]

    if is_strike(game[i+1]):
        return game[i+1][0] + game[i+2][0]

    return False


@s.solve()
def get_frame_score(frame, game, i):

    if not is_spare(frame) and not is_strike(frame):
        return frame[0] + frame[1]

    if is_spare(frame):
        return frame[0] + frame[1] + get_next_throw(i, game)

    if is_strike(frame):
        return frame[0] + get_next_2_throws(i, game)

    return False


def get_score(game):
    """
    eg: game = ((10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,0),(10,10,10))

    """

    score = 0

    for i, frame in enumerate(game):
        score += get_frame_score(frame, game, i)

    return score
