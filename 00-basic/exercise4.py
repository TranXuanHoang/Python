"""
1) Write a normal function that accepts another function as an
   argument. Output that other function in your "normal" function.

2) Call your "normal" function by passing a lambda function – which
   performs any operation of your choice – as an argument.

3) Tweak your normal function by allowing an infinite amount of
   arguments on which your lambda function will be executed.     

4) Format the output of your "normal" function such that numbers look
   nice and are centered in a 20 character column.
"""


def normal_fn(other_fn, *args):
    print(other_fn)
    return [other_fn(arg) for arg in args]


halfed_numbers = normal_fn(lambda arg: arg / 2, 2.5, 4.9, 10, 12.3, 22.7)
for num in halfed_numbers:
    print(f'"{num:^20.1f}"')
