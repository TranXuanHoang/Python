# Lists

# Basics
foods = ['rice', 'Meat', 'vegetables', 'Eggs']
print(foods)

# Same as foods[len(foods):] = ['butter']
foods.append('butter')
print(foods)

# Same as foods[len(foods):] = ['tomatoes', 'chili sauce']
foods.extend(['tomatoes', 'Chili sauce'])
print(foods)

# Reverse order of elements in the list
foods.reverse()
print(foods)

# Copy the list
copy_of_foods = foods.copy()
print(copy_of_foods)

# Sort in ascending order
foods.sort()
print(foods)

# Sort in descending order without considering lower or upper case
copy_of_foods.sort(key=str.lower, reverse=True)
print(copy_of_foods)


# Using Lists as Stacks
stack_normal = ['+', 4, '*', 7, '-', 3, 6]
stack_error = ['+', 4, '?', 7, '-', 3, 6]


def evaluate(stack):
    expression = ''
    round = 0
    while len(stack) >= 3:
        first_operand = stack.pop()
        second_operand = stack.pop()
        operator = stack.pop()

        subexpression = str(first_operand) + ' ' + operator + \
            ' ' + str(second_operand)
        if round == 0:
            expression = '(' + subexpression + ')'
        else:
            expression = '(' + expression + ' ' + operator + \
                ' ' + str(second_operand) + ')'
        round += 1

        if operator == '+':
            stack.append(first_operand + second_operand)
        elif operator == '-':
            stack.append(first_operand - second_operand)
        elif operator == '*':
            stack.append(first_operand * second_operand)
        elif operator == '/':
            stack.append(first_operand / second_operand)
        else:
            stack.append('Error [Invalid Operator]: ' + subexpression)
            break

    result = str(stack.pop())
    if 'Error' in result:
        return result
    else:
        return expression + ' = ' + result


print(evaluate(stack_normal))
print(evaluate(stack_error))


# Using List as Queues
from collections import deque
queue = deque(["(", "c", "+", "d", ")"])
print(queue)

queue.append('/')
queue.append('d')
print(queue)

queue.appendleft('*')
queue.appendleft('a')
print(queue)


# List Comprehensions
drinks = ['   Beer ', ' Tea', 'Coca Cola  ', ' Pepsi', 'Water']

trimmed_drinks = [drink.strip()
                  for drink in drinks]  # trim all trailing spaces
print(drinks)
print(trimmed_drinks)

# filter drinks whose name length is longer that or equal to 5
print([drink for drink in trimmed_drinks if len(drink) >= 5])

foods = ['rice', 'Meat', 'vegetables', 'Eggs']
menus = [(food.upper(), drink.lower())
         for food in foods for drink in trimmed_drinks]
print(menus)

vector = [
    [1, 2, 3],
    ['Monday', 'Tuesday', 'Wednesday'],
    ['Morning', 'Afternoon', 'Night']
]

# [1, 2, 3, 'Monday', 'Tuesday', 'Wednesday', 'Morning', 'Afternoon', 'Night']
flatten_vector = [el for row in vector for el in row]
print(flatten_vector)

# [
#   [1, 'Monday', 'Morning'],
#   [2, 'Tuesday', 'Afternoon'],
#   [3, 'Wednesday', 'Night']
# ]
transposed_vector = [[row[i] for row in vector] for i in range(3)]
print(transposed_vector)
