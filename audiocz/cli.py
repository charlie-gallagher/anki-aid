from colorama import Style,Fore

GLOBAL = {
    'check': '✓',
    'x': '✘',
    'rule': '─'
}

def blue(x):
    if not isinstance(x, str):
        raise TypeError
    return f'{Fore.BLUE}{x}{Style.RESET_ALL}'


def red(x):
    if not isinstance(x, str):
        raise TypeError
    return f'{Fore.RED}{x}{Style.RESET_ALL}'


def check(x):
    if not isinstance(x, str):
        raise TypeError
    return f'{Fore.GREEN}{GLOBAL["check"]}{Style.RESET_ALL} {x}'


def fail(x):
    if not isinstance(x, str):
        raise TypeError
    return f'{Fore.RED}{GLOBAL["x"]}{Style.RESET_ALL} {x}'


def h1(x, width = 80):
    if not isinstance(x, str):
        raise TypeError
    len_x = len(x)
    prefix_len = 4
    remaining_len = width - len_x - prefix_len - 1

    prefix = GLOBAL['rule'] * 3
    tail = GLOBAL['rule'] * remaining_len
    return f'{prefix} {x} {tail}'
