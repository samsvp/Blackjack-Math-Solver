import itertools


def get_permutations(my_list):
    """
    my_list -> a list
    returns all the permutations of the list elements
    """

    new_list = [get_signal(i) + '10' if any(l in str(i) for l in ['Q','J','K'])
                                     else str(i) for i in my_list]
    
    if any(A in new_list for A in ['A','-A']):
        new_list_1 = [get_signal(i) + '11' if 'A' in i else i for i in new_list]
        new_list_2 = [get_signal(i) + '1' if 'A' in i else i for i in new_list]
        new_list = [new_list_1, new_list_2]

    if type(new_list[0]) == list:
        return list(itertools.permutations(new_list[0])) + \
               list(itertools.permutations(new_list[1]))
    else: return list(itertools.permutations(new_list))


def replace_letters(expression):
    """
    expression -> a string
    replaces the Q,J,K,A from the given expression
    """

    new_expression = expression
    for l in ['Q', 'J', 'K']: new_expression = new_expression.replace(l, '10')
    if 'A' in expression: 
        new_expression = (new_expression.replace('A', '1'), 
                          new_expression.replace('A', '11'))
    return new_expression


def get_signal(letter):
    """
    letter -> a letter with or without a signal
    returns the signal of a given letter
    """
    if len(letter) == 2: return '-'
    else: return ""


def insert_constant(expression, constant, insert_after, operator):
    """
    expression -> string expression to insert the constant
    insert_after -> a string indicating after which character to insert the
    constant. A tuple can also be passed with the char and after
    which count the constant is supposed to be insert in. (eg. (")",2) would insert 
    the constant after the second ")" in the expression)
    constant -> the constant to be inserted
    operator -> the operator that precedes the constant
    """
    if type(constant) != str: constant = str(constant)
    if type(insert_after) == str or type(insert_after) == int: insert_after = (insert_after, 1)
    
    count = 0
    for i,e in enumerate(expression):
        if e == insert_after[0]:
            count += 1
            if count == insert_after[1]:
                new_expression = expression[:i + 1] + operator + constant + expression[i + 1:]
                return new_expression
    Exception("Could not find char at the desired place.")


def solve_equation(n, op):
    """
    n -> a list of numbers (the numbers can be int or string)
    op -> a list of operators
    returns the value of the expression
    """
    assert len(n) == len(op) + 1

    expression = [str(n[i]) + op[i] for i in range(len(op))] + [str(n[-1])]
    result = eval("".join(expression))
    return result


def print_expression(numbers, op):
    """
    numbers -> list of numbers
    op -> list of mathmatical operators
    Formats the numbers and operators and prints the expression
    formed by it
    """

    expression = get_expression(numbers, op)
    print(" ".join(expression))


def print_answer(expression, permutation, operations, join_op):
    """
    expression -> a string representing the mathmatical expression of the answer
    permutation -> a list containing the permutation of the numbers that gives the right answer
    operations -> list of list of mathematical operators
    join_op -> operator to join the expressions
    Prints the problem answer
    """
    print("expression:", expression)
    l = 0
    print("answer:")
    print_expression(permutation[:len(operations[0]) + 1], operations[0])
    for i in range(len(join_op)):
        l += len(operations[i]) + 1
        print(join_op[i])
        print_expression(permutation[l : l + len(operations[i + 1]) + 1], operations[i + 1])


def get_expression(numbers, op):
    """
    numbers -> list of numbers
    op -> list of mathmatical operators
    Gets the expression formed by the numbers and operators
    """

    expression = [str(numbers[i]) + " " + op[i] for i in range(len(op))] + \
                [str(numbers[-1])]
    return expression


def _solve(numbers, operations, result=21):
    """
    numbers -> list of numbers
    operations -> list of mathematical operators
    result -> desired result
    returns the right order of numbers given the operations
    and desired result
    """
    permutations = get_permutations(numbers)
    for permutation in permutations:
        if solve_equation(permutation, operations) == result: 
            print_expression(permutation, operations)
            return permutation
    return []


def solve(numbers, operations, result=21, join_op="", 
            constants=[], constants_op=[], tol=0.1):
    """
    numbers -> list of numbers
    operations -> list of mathematical operators or a list of list of 
    mathematical operators if join_op is different than the empty string
    result -> desired result
    join_op -> operator to join the expressions
    constants -> tuple of constants to be insert and after which char. (e.g if constants
    is [("2",1)] then the number "2" will be inserted after the first ")")
    constant_op -> operator that precedes the constant
    returns the right order of numbers given the operations
    and desired result
    """
    assert len(constants) == len(constants_op)

    if not join_op: 
        if type(operations[0] == list): operations = operations[0]
        return _solve(numbers, operations, result)

    if type(join_op) != list: join_op = [join_op]
    permutations = get_permutations(numbers)
    for permutation in permutations:
        # get the expression of a possible result
        p_result = [get_expression(permutation[:len(operations[0]) + 1], operations[0])]
        l = 0
        for i in range(len(join_op)):
            l += len(operations[i]) + 1
            p_result.append(join_op[i])
            p_result.append(get_expression(
                permutation[l : l + len(operations[i + 1]) + 1], operations[i + 1]
            ))
       
        # make the expression from the list
        expression = str(p_result)
        for chars in [('[','('),(']',')'),("'",""),(",","")]:
            expression = expression.replace(chars[0], chars[1])

        #insert constants
        for i, const in enumerate(constants):
            expression = insert_constant(expression, const[0], 
                                        (')', const[1]), constants_op[i])
        
        # Change any letter from the expression given by the constants
        expression = replace_letters(expression)

        # Case in which the constant is an 'A'
        if (type(expression) == tuple): 
            if eval(expression[0]) == result: expression = expression[0]
            elif eval(expression[1]) == result: expression = expression[1]
            else: continue

        # In case of floating point errors uncomment the line bellow
        # to see possible candidates for the answer
        # if (eval(expression) < 21 + tol) and (eval(expression) > 21 - tol): 
        #   print(expression, eval(expression))
        if eval(expression) == result:
            print_answer(expression, permutation, operations, join_op)
            return permutation

    return []


if __name__ == "__main__":
    n = ['A',8,'-K',-3,-9,-7]
    o = [['/'],['-'],['+']]
    join_op = ['*','+']
    c = [(6, 1), (4, 2)]
    c_op = ['/', '*']
    solve(n,o,21,join_op,c,c_op)