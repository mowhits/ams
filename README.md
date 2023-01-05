# ams
a very simple interpreter for my toy language ams, written in python

## structures: arithmetic expressions, boolean expressions, statements
### arithmetic expressions:
1. integer constants (`2`,`3`)
2. variables (`x`)
3. binary operations (`x - 2`)
### boolean expressions:
1. comparison expressions (`x > 1`)
2. logical expressions (`x && y`, `x || y`, `!x`)
### statements
  1. assignment statements: (all variables are global, and can only store integers)
```
x := 1  
```
  2. conditional statements:
```
if x = 1, y := 2 
else, y := 4
end
```
  3. while loops:
```
while x < 10,
x := x + 1
end
```
  4. compound statements:
```
x := 1;
y := 2
```
## some examples:

### computing a factorial:
```
n := 5; # n!
p := 1;
while n > 0,
p := p*n;
n := n - 1
end
```
### computing the nth term of a fibonacci series:
```
n := 5; # F_n
a := 1;
b := 0;
while n > 0,
c := a + b;
a := b;
b := c;
n := n - 1
end
```
## execution
`python3 ams.py <filename>.ams`

## todo
- add functions
- add local variable scoping functionality
- add for-looping
- add user input and output
- better documentation

