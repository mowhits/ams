class result:
    def __init__(self, val, pos):
        self.val = val
        self.pos = pos
    def __repr__(self):
        return f'Result({self.value}, {self.pos})'
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
        if pos < len(tokens) and tokens[pos][0] == self.value and tokens[pos][1] is self.tag:
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
            right_result = self.right(tokens, left_result)
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
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return result(None, pos)
class rep(parser):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.val)
            pos = result.pos
            result = self.parser(tokens, pos)
        return result(results, pos)
class process(parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function
    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.val = self.function(result.val)
            return result
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
            result = self.parser(tokens, pos)
            if result and result.pos == len(tokens):
                return result
            else:
                return None

class exp(parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator
    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.val, right)
        next_parser = self.separator + self.parser ^ process_next
        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result


