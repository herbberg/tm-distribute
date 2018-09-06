# -*- coding: utf-8 -*-

import tmGrammar
import tmEventSetup

from jinja2 import Environment, FileSystemLoader
from jinja2 import filters, StrictUndefined

from binascii import hexlify
from collections import OrderedDict
from distutils.version import StrictVersion

import argparse
import datetime
import shutil
import re
import uuid
import sys, os

__version__ = '0.0.2'

RegexCamelSnake1=re.compile(r'([^_])([A-Z][a-z]+)')
RegexCamelSnake2=re.compile(r'([a-z0-9])([A-Z])')

def snakecase(label, separator='_'):
    """Transformes camel case label to spaced lower case (snaked) label.
    >>> snakecase('CamelCaseLabel')
    'camel_case_label'
    """
    subbed = RegexCamelSnake1.sub(r'\1{sep}\2'.format(sep=separator), label)
    return RegexCamelSnake2.sub(r'\1{sep}\2'.format(sep=separator), subbed).lower()

def hexstr(s, bytes):
    chars = bytes * 2
    return "{0:0>{1}}".format(hexlify(s[::-1]), chars)[-chars:]

def uuid2hex(s):
    return uuid.UUID(s).hex.lower()

def murmurhash(s, bits=32):
    """Returns Murmurhash signed integer."""
    return tmEventSetup.getMmHashN(format(s))

def c_init_list(*args, **kwargs):
    """Returns C99 compliant initalizer list for C99 arrays and C99 structs."""
    values = []
    for arg in args:
        values.append(format(arg))
    for k, v in kwargs.iteritems():
        values.append('.{}={}'.format(k, v))
    return '{{{}}}'.format(', '.join([value for value in values]))

class Range(object):
    """Range object with C99 compliant initalizer list string representation."""
    c_format = '0x{:04x}'
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
    def __str__(self):
        minimum = self.c_format.format(self.minimum)
        maximum = self.c_format.format(self.maximum)
        return c_init_list(minimum, maximum)

class ObjectHelper(object):
    Types = {
        tmEventSetup.Egamma: 'eg',
        tmEventSetup.Jet: 'jet',
    }
    def __init__(self, handle):
        self.type = self.Types[handle.getType()]
        self.threshold = 0
        self.slice = Range(0, 12)
        self.eta = []
        self.phi = []
        for cut in handle.getCuts():
            type_ = cut.getCutType()
            if type_ == tmEventSetup.Threshold:
                self.threshold = cut.getMinimum().index
            elif type_ == tmEventSetup.Slice:
                self.slice = Range(cut.getMinimum().index, cut.getMaximum().index)
            elif type_ == tmEventSetup.Eta:
                self.eta.append(Range(cut.getMinimum().index, cut.getMaximum().index))
            elif type_ == tmEventSetup.Phi:
                self.phi.append(Range(cut.getMinimum().index, cut.getMaximum().index))

class ConditionHelper(object):
    CombCondition = 'comb_cond'
    Types = {
        tmEventSetup.SingleEgamma: CombCondition,
        tmEventSetup.DoubleEgamma: CombCondition,
        tmEventSetup.TripleEgamma: CombCondition,
        tmEventSetup.QuadEgamma: CombCondition,
        tmEventSetup.SingleJet: CombCondition,
        tmEventSetup.DoubleJet: CombCondition,
        tmEventSetup.TripleJet: CombCondition,
        tmEventSetup.QuadJet: CombCondition,
    }
    def __init__(self, handle):
        self.name = snakecase(handle.getName())
        self.type = self.Types[handle.getType()]
        self.objects = []
        for object_ in handle.getObjects():
            self.objects.append(ObjectHelper(object_))

class SeedHelper(object):
    Operators = {
        'NOT': 'not',
        'AND': 'and',
        'OR': 'or',
        'XOR': 'xor',
    }
    condition_namespace = 'cl'
    def __init__(self, handle):
        self.index = handle.getIndex()
        self.name = snakecase(handle.getName())
        self.expression = self.__format_expr(handle.getExpressionInCondition())
    def __format_expr(self, expr):
        # replace operators
        for k,v in self.Operators.iteritems():
            expr = re.sub(r'([\)\(\s])({})([\(\s])'.format(k), r'\1{}\3'.format(v), expr)
        # replace condition names
        def condition_rename(match):
            name = snakecase(match.group(1))
            return "{}.{}".format(self.condition_namespace, name)
        expr = re.sub(r'([\w_]+_i\d+)', condition_rename, expr)
        return expr

def c_hex(value, width=0):
    """C99 compliant hex value."""
    return '0x{0:0{1}x}'.format(value, width)

def v_hex(value, width=0):
    """Raw hex value."""
    return '{0:0{1}x}'.format(value, width)

CustomFilters = {
    'c_hex': c_hex,
    'c_init_list': lambda iterable: c_init_list(*iterable),
    'hex': v_hex,
    'hexstr': hexstr,
    'hexuuid': uuid2hex,
    'vhdl_bool': lambda b: ('false', 'true')[bool(b)],
    'mmhashn': murmurhash,
}

class TemplateEngine(object):
    """Custom tempalte engine class."""

    def __init__(self, searchpath, encoding='utf-8'):
        # Create Jinja environment.
        loader = FileSystemLoader(searchpath, encoding)
        self.environment = Environment(loader=loader, undefined=StrictUndefined)
        self.environment.filters.update(CustomFilters)

    def render(self, template, data={}):
        template = self.environment.get_template(template)
        return template.render(data)

class Distribution(object):

    def __init__(self, templates_dir, filename):
        self.templates_dir = templates_dir
        hls_dir = os.path.join(templates_dir, 'hls')
        vhdl_dir = os.path.join(templates_dir, 'vhdl')
        self.engine = TemplateEngine([hls_dir, vhdl_dir])
        self.proc = sys.argv[0]
        self.timestamp = datetime.datetime.now().isoformat().rsplit('.', 1)[0]
        self.filename = filename
        self.menu = tmEventSetup.getTriggerMenu(filename)
        self.conditions = []
        for handle in self.menu.getConditionMapPtr().values():
            self.conditions.append(ConditionHelper(handle))
        self.seeds = []
        for handle in self.menu.getAlgorithmMapPtr().values():
            self.seeds.append(SeedHelper(handle))
        # sort by index
        self.seeds.sort(key=lambda seed: seed.index)


    def hls_dir(self, path, *args):
        filename = os.path.join(*args) if len(args) else ''
        return os.path.join(path, 'hls', 'module_0', 'src', 'impl', filename)

    def vhdl_dir(self, path, *args):
        filename = os.path.join(*args) if len(args) else ''
        return os.path.join(path, 'vhdl', 'module_0', 'src', filename)

    def tv_dir(self, path, *args):
        filename = os.path.join(*args) if len(args) else ''
        return os.path.join(path, 'testvectors', filename)

    def xml_dir(self, path, *args):
        filename = os.path.join(*args) if len(args) else ''
        return os.path.join(path, 'xml', filename)

    def create_dirs(self, path):
        if os.path.isdir(path):
                raise RuntimeError("Distribution directory already exists: {}".format(path))
        if not os.path.isdir(path):
            os.makedirs(self.hls_dir(path))
            os.makedirs(self.vhdl_dir(path))
            os.makedirs(self.tv_dir(path))
            os.makedirs(self.xml_dir(path))

    def write_template(self, template, filename, data):
        with open(filename, 'w') as fp:
            base = dict(
                meta=dict(
                    proc=dict(
                        name=self.proc,
                        version=StrictVersion(__version__)
                    ),
                    timestamp=self.timestamp,
                ),
                menu=dict(
                        name=self.menu.getName(),
                        uuid=self.menu.getMenuUuid(),
                        dist_uuid=self.menu.getFirmwareUuid(),
                ),
                module=dict(
                    id=0,
                )
            )
            base.update(data)
            content = self.engine.render(template, base)
            fp.write(content)

    def write_cuts(self, path):
        template = 'cuts.hxx'
        filename = self.hls_dir(path, template)
        data = {
            'conditions': self.conditions
        }
        self.write_template(template, filename, data)

    def write_conditions(self, path):
        template = 'conditions.hxx'
        filename = self.hls_dir(path, template)
        data = {
            'conditions': self.conditions
        }
        self.write_template(template, filename, data)

    def write_seeds(self, path):
        template = 'seeds.hxx'
        filename = self.hls_dir(path, template)
        data = {
            'seeds': self.seeds,
            'condition_namespace': SeedHelper.condition_namespace
        }
        self.write_template(template, filename, data)

    def write_menu(self, path):
        template = 'menu.hxx'
        filename = self.hls_dir(path, template)
        data = {}
        self.write_template(template, filename, data)

    def write_constants(self, path):
        template = 'constants_pkg.vhd'
        filename = self.vhdl_dir(path, template)
        data = {
            'seeds': self.seeds,
        }
        self.write_template(template, filename, data)

    def write_xml(self, path, dist):
        shutil.copyfile(self.filename, self.xml_dir(path, '{}-d{}.xml'.format(self.menu.getName(), dist)))

    def write_impl(self, path, dist):
        path = os.path.join(path, '{}-d{}'.format(self.menu.getName(), dist))
        self.create_dirs(path)
        self.write_cuts(path)
        self.write_conditions(path)
        self.write_seeds(path)
        self.write_menu(path)
        self.write_constants(path)
        self.write_xml(path, dist)
