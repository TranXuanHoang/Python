# FUNCTIONS

# Positional-Only Arguments
def pos_only(arg1, arg2, /):
    print(f'{arg1}, {arg2}')


pos_only('One', 2)

# Cannot pass keyword arguments to a function of positional-only arguments
# pos_only(arg1='One', arg2=2)


# Keyword-Only Arguments
def kw_only(*, arg1, arg2):
    print(f'{arg1}, {arg2}')


kw_only(arg1='First', arg2='Second')
kw_only(arg2=2, arg1=1)

# Cannot pass arguments without their name being specified specifically
# kw_only(1, arg1=2)


# No Restriction On Positional-Only Or Keyword-Only Arguments
def no_res(arg1, arg2):
    print(f'{arg1}, {arg2}')


# Positional arguments will always need to be placed in front of keyword arguments
no_res('Firstly', arg2='Secondly')


# Combine Both Positional-Only, Positional-Or-Keyword and Keyword-Only Arguments
def fn(pos1, pos2, /, pos_or_kw1, pos_or_kw2, *, kw1, kw2):
    print(f'{pos1}, {pos2}, {pos_or_kw1}, {pos_or_kw2}, {kw1}, {kw2}')


fn(1, 'Two', 3, pos_or_kw2='Four', kw1=5, kw2='Six')


# Arbitrary Argument Lists
def hyper_link(protocol, domain, *routes, separator='/'):
    return f'{protocol}://{domain}/' + separator.join(routes)


print(hyper_link('https', 'python.org', 'downloads',
                 'release', 'python-385', separator='/'))


# Unpacking List/Tuple Argument Lists with * and Dictionary Arguments with **
def server(host, port, separator=':'):
    return f'{host}{separator}{port}'


print(server(*['localhost', 8080]))  # call with arguments unpacked from a list


def url(routes, params):
    r = '/'.join(routes)
    p = '&'.join([f'{name}={value}' for name, value in params.items()])
    return f'{r}?{p}'


route_config = {
    'routes': ['download', 'latest'],
    'params': {
        'ver': 3,
        'os': 'windows'
    }
}

print(url(**route_config))  # call with arguments unpacked from a dictionary


# Lambda Expressions
week_days = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
day_codes = [3, 5, 2, 6, 1, 7]


def convert_days(converter_fn, day_codes):
    return [converter_fn(day_code) for day_code in day_codes]


converted_days = convert_days(
    lambda day_code: week_days[day_code % 7], day_codes)
print(converted_days)
