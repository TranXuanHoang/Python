"""
1) Import the random function and generate both a random number
   between 0 and 1 as well as a random number between 1 and 10.

2) Use the datetime library together with the random number to
   generate a random, unique value.
"""

import random
from datetime import datetime
import time

rand_num1 = random.random()
print(rand_num1)

rand_num2 = random.randint(1, 10)
print(rand_num2)

# Print current datetime in a form like '2020-07-24 19:17:35.963878'
print(datetime.now())

# Get the current time in seconds since the Epoch
print(time.time())


def gen_unique_value():
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S%f')
    return f'{current_datetime}.{rand_num2}'


print(gen_unique_value())
