import tmEventSetup
import re

# Precompiled regular expressions for function snakecase
snakecase_regex1 = re.compile(r'([^_])([A-Z][a-z]+)')
snakecase_regex2 = re.compile(r'([a-z0-9])([A-Z])')

def snakecase(label, separator='_'):
    """Transformes camel case label to spaced lower case (snaked) label.
    >>> snakecase('CamelCaseLabel')
    'camel_case_label'
    """
    subbed = snakecase_regex1.sub(r'\1{sep}\2'.format(sep=separator), label)
    return snakecase_regex2.sub(r'\1{sep}\2'.format(sep=separator), subbed).lower()

def murmurhash(s, bits=32):
    """VHDL compliant murmurhash unsigned integer.
    >>>murmurhash('spam')
    1491563546L
    """
    return tmEventSetup.getMmHashN(format(s))
