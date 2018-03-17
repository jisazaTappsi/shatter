import re

from testa.tokens import TOKENS, get_token_sequence


def sub_str(v, p1, p2):
    """
    returns substring if all reasonable conditions met otherwise None.
    :param v: MyString object.
    :param p1: position index
    :param p2: position index
    :return: substring
    """
    if p1 is not None and p2 is not None and 0 <= p1 <= len(v) and 0 <= p2 <= len(v):
        return v[p1, p2]

    return None


def sub_str_2(v, r, c):
    """
    Return cth match of regex in v.
    :param v: MyString
    :param r: Regex
    :param c: cth match of regex in v.
    :return: string
    """

    # Where the cth match starts
    p1 = v.pos(TOKENS['empty'], r, c)

    # Where the cth match ends
    p2 = v.pos(r, TOKENS['empty'], c)

    return sub_str(v, p1, p2)


def match(v, r, k):
    """
    Has at least k matches.
    :param v: MyString
    :param r: regex
    :param k: integer. It is the minimum number of matches.
    :return:
    """
    return len(re.findall(r, str(v))) >= k


class MyString:

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s

    def __len__(self):
        return len(self.s)

    def __eq__(self, other):
        if isinstance(other, MyString):
            return self.s == other.s
        elif isinstance(other, str):
            return self.s == other
        else:
            return False

    def __getitem__(self, item):

        if isinstance(item, tuple) and len(item) > 1:
            return MyString(self.s[item[0]:item[1]])
        elif isinstance(item, int):
            return self.s[item]
        elif isinstance(item, slice):
            if item.step is None:
                return self.s[item.start: item.stop]
            else:
                return self.s[item.start: item.step]
        else:
            return NotImplemented('Fuck off')

    def c_pos(self, k):
        """
        Index, including negative case (from the right side).
        :param k:
        :return:
        """
        if k >= 0:
            return k
        else:
            # TODO: bug here for k=-1. Will be out of range!
            return len(self.s) + k + 1

    def pos(self, r1, r2, c):
        """
        Find the index t for the cth occurrence of: Matching the suffix of s[:t] and the prefix of s[t:]
        If c is negative reverses the string and returns 'len(s) - t + 1' instead of 't'
        :param r1: regex1
        :param r2: regex2
        :param c: integer, the occurrence number
        :return: index.
        """

        # c is a non-zero integer
        if isinstance(c, str):
            c = eval(c)

        # reverse string if c is negative.
        if c < 0:
            s = ''.join([e for e in reversed(self.s)])
            c = abs(c)
            is_reversed = True
        else:
            s = self.s
            is_reversed = False

        match_number = 0
        for t, _ in enumerate(s):
            s1 = s[:t]
            s2 = s[t:]

            # matches suffix
            match1 = re.findall(r1 + '$', s1)

            # matches prefix
            match2 = re.findall('^' + r2, s2)

            if len(match1) > 0 and len(match2) > 0:
                match_number += 1
                if match_number == c:
                    if is_reversed:
                        return len(s) - t + 1
                    else:
                        return t

        return None

    @staticmethod
    def loop(lambda_function):
        """
        Concatenates stuff created by the lambda function until the output of this function is None.
        :param lambda_function: a function with a w integer input.
        :return: MyString object.
        """
        concat = ''
        w = 0

        # do while loop.
        while True:
            o = lambda_function(w + 1)
            if o is None:
                break
            else:
                concat += o
                w += 1

        return MyString(concat)


def switch(*args):
    """
    Given each arg as a tuple (b, e) returns the first match. This is equivalent to
    if b1:
        return e1
    elif b2:
        :return e2
        ...
    :param args: are in the form ((b1, e1), (b2, e2) ...)
    :return: one of the e
    """

    for b, e in args:
        if b:
            return e


def concatenate(*args):
    """
    If no argument is None, then join all strings.
    :param args: Can be strings, MyString objects or None
    :return: None or string.
    """
    for e in args:
        if e is None:
            return None

    return ''.join([str(e) for e in args])


def example_2(s):
    v = MyString(s)
    return sub_str(v, v.pos(TOKENS['empty'], TOKENS['digits'], 1), v.c_pos(-1))


def example_3(s):
    v = MyString(s)
    return sub_str(v, v.c_pos(0), v.pos(TOKENS['forward_slash'], TOKENS['empty'], -1))


def example_4(s):
    v = MyString(s)
    return str(v.loop(lambda w: concatenate(sub_str_2(v, TOKENS['uppercase'], w))))


def example_5(s):
    v = MyString(s)

    def lambdasuri(w):
        s1 = get_token_sequence(TOKENS['digits'], TOKENS['forward_slash'])
        s2 = get_token_sequence(TOKENS['forward_slash'], TOKENS['digits'])
        p1 = v.pos(TOKENS['left_parenthesis'], s1, w)
        p2 = v.pos(s2, TOKENS['right_parenthesis'], w)
        return concatenate(sub_str(v, p1, p2), ' #')

    return str(v.loop(lambdasuri))


def example_6(s):
    v = MyString(s)

    def lambdasuri(w):
        # TODO: what the fuck is '[^ ]' ?
        p1 = v.pos(TOKENS['space'], '[^ ]', w)
        p2 = v.pos('[^ ]', TOKENS['space'], w)
        return concatenate(sub_str(v, p1, p2), ' ')

    res = v.loop(lambdasuri)

    return sub_str(res, 0, len(res) - 1)


def example_7(s1, s2):
    v1 = MyString(s1)
    v2 = MyString(s2)

    b1 = match(v1, TOKENS['all_chars'], 1) and match(v2, TOKENS['all_chars'], 1)
    e1 = concatenate(v1, '(', v2, ')')
    b2 = not match(v1, TOKENS['all_chars'], 1) or not match(v2, TOKENS['all_chars'], 1)
    e2 = ''
    return switch((b1, e1), (b2, e2))


if __name__ == '__main__':

    assert example_2('BTR KRNL WK CORN 15Z') == '15Z'
    assert example_2('CAMP DRY DBL NDL 3.6 OZ') == '3.6 OZ'
    assert example_2('CHORE BOY HD SC SPNG 1 PK') == '1 PK'

    out = example_3('Company/Code/index.html')
    assert out == 'Company/Code/'

    out = example_3('Company/Docs/Spec/specs.doc')
    assert out == 'Company/Docs/Spec/'

    out = str(example_4('International Business Machines'))
    assert out == 'IBM'

    out = example_4('Principles Of Programming Languages')
    assert out == 'POPL'

    out = example_5('(6/7)(4/5)(14/1)')
    assert out == '6/7 #4/5 #14/1 #'

    out = example_5('49(28/11)(14/1)')
    assert out == '28/11 #14/1 #'

    out = example_5('() (28/11)(14/1)')
    assert out == '28/11 #14/1 #'

    out = example_6('    something     with    lots of spaces    ')
    assert out == 'something with lots of spaces'

    out = example_7('Alex', 'Asst.')
    assert out == 'Alex(Asst.)'

    out = example_7('', 'Manager')
    assert out == ''

    out = example_7('Alex', '')
    assert out == ''