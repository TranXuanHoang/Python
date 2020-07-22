"""
1) Create a list of names and use a for loop to output the length of each name (len()).

2) Add an if  check inside the loop to only output names longer than 5 characters.

3) Add another if  check to see whether a name includes a “n”  or “N”  character.

4) Use a while  loop to empty the list of names (via pop())
"""

names = ['Bob', 'Chris', 'Micheal', 'David',
         'Fernando Torres', 'Thomas Muller', 'Wendy']


def contains(name, patterns):
    for pattern in patterns:
        if pattern in name:
            return True
    return False


for name in names:
    print(len(name))

for name in names:
    if len(name) > 5:
        print(name)

for name in names:
    if len(name) > 5 and contains(name, ['n', 'N']):
        print(name)

while len(names) > 0:
    names.pop()
print(names)
