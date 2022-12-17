import lexer

RESERVED = 'RESERVED'
INT = 'INT'
IDENT = 'IDENT'

token_exprs = [
        (r'\s', None),
        (r'#\w*', None), # ignores comments
        (r'\:=', RESERVED), # assignment operator
        (r'\(', RESERVED), # opening bracket
        (r'\)', RESERVED), # closing bracket
        (r'\;', RESERVED), # compound statement delimiter
        (r'\,', RESERVED), # do/then equivalent
        (r'\+', RESERVED), # addition operator
        (r'\-', RESERVED), # subtraction operator
        (r'\*', RESERVED), # multiplication operator
        (r'\/', RESERVED), # division operator 
        (r'\*\*', RESERVED), # exponentiation operator
        (r'=', RESERVED), # equals to comparator
        (r'<', RESERVED), # less than comparator
        (r'>', RESERVED), # greater than comparator
        (r'<=', RESERVED), # less than equal to comparator
        (r'>=', RESERVED), # greater than equal to comparator
        (r'\&\&', RESERVED), # and logical operator
        (r'\|\|', RESERVED), # or logical operator
        (r'\^\^', RESERVED), # xor logical operator
        (r'!', RESERVED), # not logical operator
        ('if', RESERVED), 
        ('else', RESERVED),
        ('while', RESERVED),
        ('end', RESERVED),
        (r'[0-9]+', INT), # integers
        (r'[A-Za-z][A-Za-z0-9_]*', IDENT), # identifiers (starts with character, only numerals and underscore allowed)
        ]
def ams_lex(chars):
    return lexer.lex(chars, token_exprs)

