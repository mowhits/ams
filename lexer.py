import sys
import re

def lex(chars, token_exprs):
    pos = 0
    tokens = []
    while pos < len(chars):
        matching = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            matching = regex.match(chars, pos)
            if matching:
                text = matching.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
            if not matching:
                sys.stderr.write(f'Illegal character: {chars[pos]}')
                sys.exit(1)
            else:
                pos = matching.end(0)
    return tokens
