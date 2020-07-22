"""
1) Define two variables – one to save user's name and one to save user's age

2) Create 2 functions with each to get name and age from the command prompt

3) Create a function which prints the name and age

4) Create a function which calculates and returns the number of decades
   the user already lived (e.g. 34 = 3 decades)
"""

name = ''
age = 0


def get_name():
    return input('Your name: ')


def get_age():
    return int(input('Your age: '))


def print_user_info(name, age):
    print('Name: ' + name + '\nAge: ' + str(age))


def decades_lived(age):
    return age // 10


name = get_name()
age = get_age()
decades = decades_lived(age)
print_user_info(name=name, age=age)
print('Decades Lived: ' + str(decades))
