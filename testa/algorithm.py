import re

from testa.dsl import MyString, sub_str
from testa.tokens import TOKENS


# ------------------------------------ LETS ROCK!!! ------------------------------------


# 'BTR KRNL WK CORN 15Z') -> '15Z'


def get_edges(s):
    edges = set()
    for i in range(len(s)-1):
        for j in range(i + 1, len(s)):
            edges.add((i, j))

    return edges


def make_partitions(s):
    partitions = dict()

    for k, t in TOKENS.items():

        res = ''.join(re.findall(t, str(s)))

        if partitions.get(res) is not None:  # old partition
            partitions[res] += t
        else:  # new partition.
            partitions[res] = [t]

    return partitions


def get_partitions_representatives(s):
    return {e[0] for e in make_partitions(s).values()}


def get_matching_tokens(s, k, suffix):
    """
    Gets set of all pairs: (token_sequence, k'), where k' is index of s.
    :param s: string
    :param k: position
    :param suffix: Boolean. If True matches substring after index else matches before index.
    :return: pairs.
    """
    pairs = set()
    for index, _ in enumerate(s):

        if suffix:
            substring = s[index:k]
        else:
            substring = s[k:index - 1]

        open_tokens = get_partitions_representatives(s)
        open_tokens.difference([TOKENS['empty'], TOKENS['start'], TOKENS['end']])
        outputs = set()

        while len(open_tokens) > 0:

            t = open_tokens.pop()
            res = tuple(re.findall(t, substring))

            if len(res) > 0:
                if res not in outputs:
                    outputs.add(res)
                    pairs |= {(t, index)}

                    my_set = set()
                    for e in open_tokens:
                        if t not in e:
                            my_set.add(e + t)
                    open_tokens |= my_set
                    #open_tokens |= {e + t for e in open_tokens if t not in e}

    return pairs


# TODO: don't know how to do this.
#def generate_regex(r, s):

    #result = ''
    #for token in r:
    #    result +=

    #return result


def generate_position(s, k):
    result = {s.c_pos(k), s.c_pos(-(len(s)-k))}

    r1_matches = get_matching_tokens(s, k, suffix=True)  # matches substring suffix.
    r2_matches = get_matching_tokens(s, k, suffix=False)  # matches substring prefix.

    for r1, k1 in r1_matches:
        for r2, k2 in r2_matches:

            r12 = r1 + r2

            # Tries increasing c values until it gets it.
            for c in range(1, len(s)):
                if k == s.pos(r1, r2, c):
                    break

            c_prime = len(re.findall(r12, str(s)))

            # TODO:
            #r1_set = generate_regex(r1, s)
            #r2_set = generate_regex(r2, s)

            result |= {s.pos(r1, r2, c), s.pos(r1, r2, -(c_prime - c + 1))}

    return result


def generate_substring(sigma, s):

    result = set()
    positions = [m.span()[0] for m in re.finditer(s, str(sigma))]
    for p in positions:
        y1 = generate_position(sigma, p)
        y2 = generate_position(sigma, p + len(s))

        for y1_e in y1:
            for y2_e in y2:
                result.add(sub_str(s, y1_e, y2_e))

        #result |= sub_str(s, y1, y2)

    return result


def get_w(edges, s, sigma):
    w = {}
    for i, j in edges:
        w[(i, j)] = {s[i:j]} | generate_substring(sigma, s[i:j])

    return w


def generate_str(sigma, s):
    nodes = {i for i in range(len(s))}
    source_nodes = {0}
    target_nodes = {len(s)}
    edges = get_edges(s)
    w = get_w(edges, s, sigma)

    print(w)


generate_str(MyString('BTR KRNL WK CORN 15Z'), MyString('15Z'))
