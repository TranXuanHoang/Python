"""
Simulate a terminal prompting for user commands. Each time user entered a new command,
save it into a file in local hard disk so that next time when the user runs the program,
all command he/she typed in the past can be refered again by issuing the following command:
  rf    - read the whole commands
  rf n  - read the most current 'n' commands

Ask the username and the type of the file at the beginning of each terminal session to
determine which file type to use during that session. File type should only either
'json' (JSON file - human readable) or 'bin' (binary file)
"""
import json
import pickle
import re
import math

commands = []
json_file_name = '06_files.json'
binary_fine_name = '06_files.bin'


def ask_for_username():
    return input('Username: ')


def ask_for_file_type():
    """ Ask the user to provide the type of the file to which data will be saved

    Should be either 'json' (for text file in JSON format) or 'bin' (for binary file)"""
    while True:
        file_type = input('Type of the file to store data (json/bin): ')
        if file_type != 'json' and file_type != 'bin':
            continue
        else:
            return file_type


def get_user_input(username, session_id):
    """ Prompt and get a command from the user.

    Arguments:
        :username: The username of the user.
        :session_id: The session number incremented each time asking for inputing a command.
    Returns:
        The string command the user entered.
    """
    print('\nrf [n]: read file content [with last n lines], q: quit')
    return input(f'[{session_id:^3}@{username}] $ ')


def save_to_file(file_name):
    """ Save data into a JSON file (text tha can be read by human) 
    that will be stored in local hard disk.

    Arguments:
        :file_name: The name of the file to which data will be saved.
    """
    with open(file_name, mode='w') as f:
        f.write(json.dumps(commands))


def save_to_binary_file(file_name):
    """ Save data into a file that will be stored in local hard disk.

    Arguments:
        :file_name: The name of the file to which data will be saved.
    """
    with open(file_name, mode='wb') as f:
        f.write(pickle.dumps(commands))


def read_from_file(file_name, lines='All'):
    """ Read data from a text file (human readable) and print out the
    most currently entered commands.

    Arguments:
        :file_name: The name of the text file to be read.
        :lines: The number of the most currently entered commands that will be printed out.
    """
    with open(file_name, mode='r') as f:
        global commands
        commands = json.loads(f.readlines()[0])

        num_of_lines = len(commands) if lines == 'All' else int(lines)
        printed_commands = commands[-num_of_lines:]
        for command in printed_commands:
            print(command)


def read_from_binary_file(file_name, lines='All'):
    """ Read data from a binary file and print out the most currently entered commands.

    Arguments:
        :file_name: The name of the file to be read.
        :lines: The number of the most currently entered commands that will be printed out.
    """
    with open(file_name, mode='rb') as f:
        global commands
        commands = pickle.loads(f.read())

        num_of_lines = len(commands) if lines == 'All' else int(lines)
        printed_commands = commands[-num_of_lines:]
        for command in printed_commands:
            print(command)


username = ask_for_username()
file_type = ask_for_file_type()
session_id = 1
readfile_command_pattern = re.compile(r'rf [1-9]{1}[0-9]*')
while True:
    command = get_user_input(username, session_id)
    commands.append(command)
    if command == 'q':
        break
    elif command == 'rf':
        print("Read whole file")
        if file_type == 'json':
            read_from_file(json_file_name)
        elif file_type == 'bin':
            read_from_binary_file(binary_fine_name)
    elif readfile_command_pattern.match(command):
        match_info = readfile_command_pattern.match(command)
        num_of_lines = f'{match_info.group(0)}'.split(' ')[1]
        print(
            f'Read {num_of_lines} {"lines" if int(num_of_lines) > 1 else "line"}')
        if file_type == 'json':
            read_from_file(json_file_name, lines=num_of_lines)
        elif file_type == 'bin':
            read_from_binary_file(binary_fine_name, lines=num_of_lines)
    else:
        print(f'Saving {command} to file')
        if file_type == 'json':
            save_to_file(json_file_name)
        elif file_type == 'bin':
            save_to_binary_file(binary_fine_name)
    session_id += 1
