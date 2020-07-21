user_info = {'name': 'Hoang', 'age': 29, 'level': 5.5,
             'majors': ['Angular', 'NodeJS', 'Python', 'Flutter']}

print(user_info)

# list(dictionary) returns a list of all keys of the dictionary
print(list(user_info))

# Check whether a key exists
print('age' in user_info)
print('weight' in user_info)

# Loop through the dictionary and get corresponding value using its key
for key in user_info:
    print(user_info[key])

# The key and corresponding value can be retrieved at the same time using the items() method
for key, val in user_info.items():
    print(str(key) + ': ' + str(val))

# Add new entry (key:value pair) to the dictionary
user_info['weight'] = '55Kg'
print(user_info)

# Remove an entry (key:value pair) from the dictionary
del user_info['level']
print(user_info)

# Dictionary comprehensions: Upper case all key:value pairs and put them into a new dictionary
new_dict = {str.upper(key): str.upper(str(val))
            for key, val in user_info.items()}
print(new_dict)

# Other ways to define dictionaries
operating_systems = dict(
    [('Android', 'Pie'), ('iOS', 13.6), ('Windows', 10), ('macOS', 'Catalina')])
print(operating_systems)

ingredients = dict(sugar='15g', meat='1Kg', tomatoes=3)
print(ingredients)
