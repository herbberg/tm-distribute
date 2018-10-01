from binascii import hexlify
import uuid

def boolean(value):
    """VHDL compliant boolean representation.

    >>> boolean(0)
    'false'
    """
    return ('false', 'true')[bool(value)]

def hex(value, width=0):
    """VHDL compliant hex value.

    >>> hex(42, width=8)
    '0000002a'
    """
    return '{0:0{1}x}'.format(value, width)

def hexstr(s, bytes):
    """VHDL compliant hex encoded string.

    >>> hexstr('spam', bytes=8)
    '000000006d617073'
    """
    chars = bytes * 2
    return "{0:0>{1}}".format(hexlify(s[::-1]), chars)[-chars:]

def hexuuid(s):
    """VHDL compliant hex encoded UUID.

    >>> uuid2hex('d323e4e5-b140-414b-a63b-d29346566969')
    'd323e4e5b140414ba63bd29346566969'
    """
    return uuid.UUID(s).hex.lower()
