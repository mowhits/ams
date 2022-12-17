class result:
    def __init__(self, val, pos):
        self.val = val
        self.pos = pos
    def __repr__(self):
        return f'Result({self.val}, {self.pos})'
class parser:
    def __call__(self, tokens, pos):
        return None
    def __add__(self, other):
        return concat(self, other)
    def __mul__(self, other):
        return exp(self, other)
    def __or__(self, other):
        return alternate(self, other)
    def __xor__(self, function):
        return process(self, function)

class reserved(parser):
    def __init__(self, val, tag):
        self.val = val
        self.tag = tag
    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.val and tokens[pos][1] is self.tag:
            return result(tokens[pos][0], pos + 1)
        else:
            return None

class tag(parser):
        def __init__(self, tag):
            self.tag = tag
        def __call__(self, tokens, pos):
            if pos < len(tokens) and tokens[pos][1] is self.tag:
                return result(tokens[pos][0], pos + 1)
class concat(parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_val = (left_result.val, right_result.val)
                return result(combined_val, right_result.pos)

class alternate(parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result

class opt(parser):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, tokens, pos):
        Result = self.parser(tokens, pos)
        if Result:
            return Result
        else:
            return result(None, pos)

class rep(parser):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, tokens, pos):
        Results = []
        Result = self.parser(tokens, pos)
        while result:
            Results.append(Result.val)
            pos = Result.pos
            Result = self.parser(tokens, pos)
        return result(Results, pos)

class process(parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function
    def __call__(self, tokens, pos):
        Result = self.parser(tokens, pos)
        if Result:
            Result.val = self.function(Result.val)
            return Result

class lazy(parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func
    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)

class phrase(parser):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, tokens, pos):
            Result = self.parser(tokens, pos)
            if Result and Result.pos == len(tokens):
                return Result
            else:
                return None

class exp(parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator
    def __call__(self, tokens, pos):
        Result = self.parser(tokens, pos)
        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(Result.val, right)
        next_parser = self.separator + self.parser ^ process_next
        next_result = Result
        while next_result:
            next_result = next_parser(tokens, Result.pos)
            if next_result:
                Result = next_result
        return Result

