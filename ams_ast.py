from equality import *

# defining arithmetic expression classes
class artexp(equality):
    pass
class intartexp(artexp): # integer constants
    def __init__(self, i):
        self.i = i
    def __repr__(self):
        return f'intartexp({self.i})'
    def eval(self, env):
        return self.i

class varartexp(artexp): # variables
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'varartexp({self.name})'
    def eval(self, env):
        if self.name in env:
            return env[self.name]

class binartexp(artexp): # binary operations
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f'binartexp({self.left},{self.operator}, {self.right})'
    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        if self.operator == '+':
            value = left_val + right_val
        elif self.operator == '-':
            value = left_val - right_val
        elif self.operator == '*':
            value = left_val * right_val
        elif self.operator == '/':
            value = left_val / right_val
        elif self.operator == '**':
            value = left_val ** right_val
        else:
            raise RuntimeError(f'Unknown operator {self.operator}')
        return value

# defining boolean expression classes

class boolexp(equality): 
    pass
class relboolexp(boolexp): # relational bool exps
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f'relboolexp({self.left}, {self.operator}, {self.right})'
    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        if self.operator == '<':
            value = left_val < right_val
        elif self.operator == '<=':
            value = left_val <= right_val
        elif self.operator == '>':
            value = left_val > right_val
        elif self.operator == '>=':
            value = left_val >= right_val
        elif self.operator == '=':
            value = left_val == right_val
        elif self.operator == '!=':
            value = left_val != right_val
        else:
            raise RuntimeError(f'Unknown operator {self.operator}')
        return value

class andboolexp(boolexp): # and operator
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f'andboolexp({self.left}, {self.right})'
    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        return left_val and right_val

class orboolexp(boolexp): # or operator
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f'orboolexp({self.left}, {self.right})'
    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        return left_val or right_val

class notboolexp(boolexp): # not operator
    def __init__(self, exp):
        self.exp = exp
    def __repr__(self):
        return f'notboolexp({self.exp})'
    def eval(self, env):
        val = self.exp.eval(env)
        return not val

# defining statement classes

class stat(equality):
    pass

class assignmentstat(stat): # assignment statements
    def __init__(self, name, artexp):
        self.name = name
        self.artexp = artexp
    def __repr__(self):
        return f'assignmentstat({artexp})'
    def eval(self, env):
        val = self.Artexp.env(env)
        env[self.name] = val

class compoundstat(stat): # compound statements
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def __repr__(self):
        return f'compoundstat({self.first}, {self.second})'
    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

class ifstat(stat): # if-else statements
    def __init__(self, cond, true_stat, false_stat):
        self.cond = cond
        self.true_stat = true_stat
        self.false_stat = false_stat
    def __repr__(self):
        return f'ifstat({self.cond}, {self.true_stat}, {self.false_stat})'
    def eval(self, env):
        cond_val = self.cond.eval(env)
        if cond_val:
            self.true_stat.eval(env)
        elif self.false_stat:
            self.false_stat.eval(env)

class whilestat(stat): # while loop statements
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    def __repr__(self):
        return f'whilestat({self.cond}, {self.body})'
    def eval(self, env):
        cond_val = self.cond.eval(env)
        while cond_val:
            self.body.eval(env)
            cond_val = self.cond.eval(env)

