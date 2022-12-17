import sys
from ams_lexer import *

if __name__ == '__main__':
    filename= sys.argv[1]
    file = open(filename)
    chars = file.read()
    file.close()
    tokens = ams_lex(chars)
    for token in tokens:
        print(token)


