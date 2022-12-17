from functools import reduce
from ams_combinators import *
from ams_lexer import *
from ams_ast import *

def keyword(k): # parses reserved keywords
    return reserved(k, RESERVED)

ident = tag(IDENT) # parses identifiers

num = tag(INT) ^ (lambda i: int(i)) # parses integers

# parsing arithmetic expressions

def Artexp_val(): # converts values returned by ident and num into expressions
    return (num ^ (lambda i: intartexp(i))) | (ident ^ (lambda var: varartexp(var)))

def process_group(parsed): # combines grouped expressions
    ((_, p), _) = parsed
    return p

def Artexp_group(): # parses grouped arithmetic expressions
    return keyword('(') + lazy(Artexp) + keyword(')') ^ process_group

def Artexp_term(): # parses terms of expression
    return Artexp_val | Artexp_group

def process_bin(operator): # combines expressions with arithmetic operator
    return lambda l, r: binartexp(l, operator, r)

def any_operator_in_list(operators): # returns parser which matches any of the operators
    operator_parsers = [keyword(operator) for operator in operators]
    parser = reduce(lambda l, r: l | r, operator_parsers)
    return parser

Artexp_precedence = [['**'], ['*', '/'], ['+', '-']] # defines operator precedence (highest first)

def precedence(val_parser, precedence_levels, combine): # takes in terms, operators, and combines them following precedence for both arithmetic and boolean expressions
    def operator_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = val_parser * operator_parser(precedence_levels[0])
    for precedence_level in precedence_level[1:]:
        parser = parser * operator_parser(precedence_level)
    return parser

def Artexp(): # parses arithmetic expression with precedence
    return precedence(Artexp_term(), Artexp_precedence, process_bin)


def process_rel(parsed): # combines expressions with relational operator
    ((left, operator), right) = parsed
    return Relboolexp(left, operator, right)

# parsing logical and relational bool exps

def Relboolexp(): # parses relational expressions
    rels = ['<', '<=', '=', '!=', '>=', '>']
    return Artexp() + any_operator_in_list(rels) + Artexp() ^ process_rel

def Boolexp_not(): # defines not expression
    return keyword('!') + lazy(Boolexp_term) ^ (lambda parsed: notboolexp(parsed[1]))

def Boolexp_group(): # parses grouped boolean expression
    return keyword('(') + lazy(Boolexp) + keyword(')') ^ process_group

def Boolexp_term(): # parses terms of bool expression
    return Boolexp_not() | Relboolexp() | Boolexp_group()

Boolexp_precedence = [[r'\&\&'], [r'\|\|']] # defines logical operator precedence (highest first)

def process_logic(operator): # combines expressions with logical operator
    if operator == r'\&\&':
        return lambda l, r: andboolexp(l, r)
    if operator == r'\|\|':
        return lambda l, r: orboolexp(l, r)
    else:
        raise RuntimeError(f"Unknown logic operator: {operator}")

def Boolexp(): # parses bool expressions with precedence
    return precedence(Boolexp_term(), Boolexp_precedence, process_logic)


# parsing statements

def assign_stat(): # parses assignment statements
    def Process(parsed):
        ((name, _), exp) = parsed
        return assignmentstat(name, exp)
    return ident + keyword(':=') + Artexp() ^ Process

def stat_list(): # parses compound statements
    separator = keyword(';') ^ (lambda x: lambda l, r: compoundstat(l, r)) # using exp to avoid left recursion
    return exp(stat(), separator)

def if_stat(): # parses if statements
    def Process(parsed):
        (((((_, condition), _), true_stat), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stat) = false_parsed
        else:
            false_stat = None
        return ifstat(condition, true_stat, false_stat)
    return keyword('if') + Boolexp() + keyword(',') + lazy(stat_list) + opt(keyword('else') + lazy(stat_list)) + keyword('end') ^ process # optional else clause

def while_stat():
    def Process(parsed):
        ((((_, condition), _), body), _) = parsed
        return whilestat(condition, body)
    return keyword('while') + Boolexp() + keyword(',') + lazy(stat_list) + keyword('end') ^ Process

def stat():
    return assign_stat() | if_stat() | while_stat()

# top level parser

def parser(): # parses entire program, ignores garbage tokens
    return phrase(stat_list())

def ams_parse(tokens):
    ast = parser()(tokens, 0)
    return ast


