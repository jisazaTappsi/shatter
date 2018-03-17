# TODO: add lower + upper case alphabet

TOKENS = {'digits': '\d+',
          'lowercase': '[a-z]+',
          'uppercase': '[A-Z]+',
          'whitespaces': '\s+',
          'all_chars': '.+',
          'start': '^',
          'end': '$',
          'empty': '',
          'space': '\s',
          'hyphen': '-',
          'dot': '\.',
          'semicolon': ';',
          'colon': ':',
          'comma': ',',
          #'backslash': '\\\\',
          #'forward_slash': '/',
          'left_parenthesis': '\(',
          'right_parenthesis': '\)',
          'left_bracket': '\{',
          'right_bracket': '\}',
          }


def get_token_sequence(*args):
    return ''.join(args)
