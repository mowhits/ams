import sys
from ams_parser import *

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write(f'usage: {sys.argv[0]} filename parsername')
        sys.exit(1)
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = ams_lex(characters)
    parser = globals()[sys.argv[2]]()
    result = parser(tokens, 0)
    print(result)
