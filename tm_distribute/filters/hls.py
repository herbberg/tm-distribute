
def boolean(value):
    """C++98 compliant boolean.

    >>> boolean(False)
    'false'
    """
    return ('false', 'true')[bool(value)]

def hex(value, width=0):
    """C++98 compliant hex value.

    >>> hex(42, width=4)
    '0x002a'
    """
    return '0x{0:0{1}x}'.format(value, width)

def string(s):
    """C++98 compliant C string conversion.

    >>> string('spam')
    '"spam"'
    >>> string(42)
    '"42"'
    """
    return "\"{0}\"".format(s)

def init_list(args):
    """C99/C++98 compliant initalizer list for C99 arrays and C99 structs.

    >>> init_list([1, [2, 3]])
    '{1, {2, 3}}'
    """
    values = []
    for arg in args:
        if isinstance(arg, bool):
            arg = boolean(arg)
        elif isinstance(arg, list):
            arg = init_list(arg)
        values.append(format(arg))
    return '{{{}}}'.format(', '.join(values))

def auto(arg):
    """Returns C99/C++98 compliant value representations.

    >>> auto(True)
    'true'
    >>> auto([1,2,3])
    '{1, 2, 3}'
    >>> auto('spam')
    '"spam"'
    """
    if isinstance(arg, bool):
        return boolean(arg)
    if isinstance(arg, list):
        return init_list(*arg)
    return arg;
