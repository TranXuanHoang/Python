"""
1) Create a list of “person” dictionaries with a name, age and list of hobbies
   for each person. Fill in any data you want.

2) Use a list comprehension to convert this list of persons into a list of
   names (of the persons).

3) Use a list comprehension to check whether all persons are older than 20.

4) Copy the person list such that you can safely edit the name of the first person
   (without changing the original list).

5) Unpack the persons of the original list into different variables and output
   these variables.
"""

people = [
    {
        'name': 'Hoang',
        'age': 29,
        'hobbies': ['Games', 'Reading books', 'Drink hot water']
    },
    {
        'name': 'Chris',
        'age': 32,
        'hobbies': ['Swimming', 'Cicling', 'Anime']
    },
    {
        'name': 'Anna',
        'age': 18,
        'hobbies': ['Singing', 'Cooking']
    },
    {
        'name': 'David',
        'age': 25,
        'hobbies': ['Photographing', 'Traveling', 'Mountain Climbing']
    },
]
print(people)

person_names = [person['name'] for person in people]
print(person_names)

# Use listcomp and all()
print(all([person['age'] > 20 for person in people]))


# Copy
def copy(person):
    return {key: val for key, val in person.items()}


copied_people = [copy(person) for person in people]
copied_people[0]['name'] = 'New name'
print(copied_people)
print(people)


# Unpack
person1, person2, person3, person4 = people
print(person1)
print(person2)
print(person3)
print(person4)
