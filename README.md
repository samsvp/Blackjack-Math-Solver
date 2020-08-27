# Blackjack-Math-Solver
A solver for the game ["Blackjack Math"](https://store.steampowered.com/app/1341220/BlackJack_Math/?l=brazilian)

## Usage

### Example 1
Let's say we have the following level:

```python
J + -6 - A
-
3 + -A
```

Create a list of the numbers and letters contained in the level
e.g.
```python
numbers = ['J',-6,'A','3','-A'] # You can list the numbers as a string or as an integer
```

Then create a list of the operators used in each of the expressions in the level
e.g.
```python
# First expression 11 + 3 - 10
# Second expression -6 + -11
o = [['+','-'],['+']] 
```

In case of more than one expression then pass the join operator
e.g.
```python
# J + -6 - A
# - # <- join operator
# 3 + -A
join_op = ['-'] 
```

Then pass it to the solver
```python
solve(n, o, 21, join_op)
```
 You can also pass constants to the solver:
 constants -> tuple of constants to be insert and after which char. (e.g if constants
 is [("2",")",1)] then the number "2" will be inserted after the first ")")
 constant_op -> operator that precedes the constant
 
 e.g.
 ```python
solve(n, o, 21, join_op)
```

### More complex example
Let's try an example with constants. If we have the equation
```python
A         -K          -9
/  [/6]*   -  [4*]+    +
8         -3          -7
```
The numbers between "[]" are constants which we can not move.
First we make a list of the number and of each operator in the expressions, as well as the 
operators that join the expression:
```python
n = ['A',8,'-K',-3,-9,-7]
o = [['/'],['-'],['+']]
join_op = ['*','+']
```
We then list the constants giving their position and their operators. In this case we woulde do it
like this:
```python
c = [(6, 1), (4, 2)]
c_op = ['/', '*']
```
We then run the following line to solve the problem:
```python
solve(n,o,21,join_op,c,c_op)
```
