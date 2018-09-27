# -*- coding: utf-8 -*-

import tmGrammar
import tmEventSetup

from jinja2 import Environment, FileSystemLoader
from jinja2 import StrictUndefined

from collections import OrderedDict
from distutils.version import StrictVersion

import argparse
import datetime
import shutil
import re
import sys, os

# Formats
import filters.generic
import filters.hls
import filters.vhdl

__version__ = '0.0.5'

def cut_data_lut(data):
    """Returns list of cut data values.
    >>> cut_data_lut('0,2,3')
    [0, 2, 3]
    """
    return [int(value.strip()) for value in data.split(',')]

class Range(object):
    """Range object with C99/C++98 compliant initalizer list string representation."""
    c_format = '0x{:04x}'
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
    def __str__(self):
        minimum = self.c_format.format(self.minimum)
        maximum = self.c_format.format(self.maximum)
        return filters.hls.init_list([minimum, maximum])

class Lut(object):
    """Generic C++98 compliant look up table.
    >>> l = Lut(true, 4)
    >>> print(l)
    [false, false, false, false]
    >>> l[1] = True
    print(l)
    [false, true, false, false]
    """
    def __init__(self, value, size):
        self.values = [value for _ in range(size)]
    def __getitem__(self, key):
        return self.values[key]
    def __setitem__(self, key, value):
        self.values[key] = value
    def __len__(self):
        return len(self.values)
    def __str__(self):
        return filters.hls.init_list(self.values)

def charge_encode(value):
    """Encode charge value to HLS string literal."""
    if value in ('positive', 'pos', '1'):
        return 'POSITIVE' # positive
    if value in ('negative', 'neg', '-1'):
        return 'NEGATIVE' # negative
    return 'IGNORE' # ignore

class ObjectHelper(object):
    Types = {
        tmEventSetup.Egamma: 'eg',
        tmEventSetup.Jet: 'jet',
        tmEventSetup.Tau: 'tau',
        tmEventSetup.Muon: 'muon',
        tmEventSetup.EXT: 'external',
    }
    IsoTypes = {
        tmEventSetup.Egamma: Lut(True, 4),
        tmEventSetup.Jet: None,
        tmEventSetup.Tau: Lut(True, 4),
        tmEventSetup.Muon: Lut(True, 4),
        tmEventSetup.EXT: None,
    }
    QualTypes = {
        tmEventSetup.Egamma: None,
        tmEventSetup.Jet: None,
        tmEventSetup.Tau: None,
        tmEventSetup.Muon: Lut(True, 16),
        tmEventSetup.EXT: None,
    }
    ComparisonTypes = {
        tmEventSetup.GE: 'GE',
        tmEventSetup.NE: 'NE',
        tmEventSetup.EQ: 'EQ',
    }
    SliceTypes = {
        tmEventSetup.Egamma: Range(0, 11),
        tmEventSetup.Jet: Range(0, 11),
        tmEventSetup.Tau: Range(0, 11),
        tmEventSetup.Muon: Range(0, 7),
    }
    def __init__(self, handle):
        self.type = self.Types[handle.getType()]
        self.threshold = 0
        self.comparison_mode = self.ComparisonTypes[handle.getComparisonOperator()]
        self.slice = self.SliceTypes[handle.getType()]
        self.eta = []
        self.phi = []
        self.isolationLUT = self.IsoTypes[handle.getType()]
        self.qualityLUT = self.QualTypes[handle.getType()]
        self.charge = charge_encode('IGNORE')
        self._init_external(handle)
        for cut in handle.getCuts():
            type_ = cut.getCutType()
            if type_ == tmEventSetup.Threshold:
                self.threshold = cut.getMinimum().index
            elif type_ == tmEventSetup.Slice:
                self.slice = Range(int(cut.getMinimum().value), int(cut.getMaximum().value))
            elif type_ == tmEventSetup.Eta:
                self.eta.append(Range(cut.getMinimum().index, cut.getMaximum().index))
            elif type_ == tmEventSetup.Phi:
                self.phi.append(Range(cut.getMinimum().index, cut.getMaximum().index))
            elif type_ == tmEventSetup.Isolation:
                self.isolationLUT = Lut(False, 4)
                for key in cut_data_lut(cut.getData()):
                    self.isolationLUT[key] = True
            elif type_ == tmEventSetup.Quality:
                self.qualityLUT = Lut(False, 16)
                for key in cut_data_lut(cut.getData()):
                    self.qualityLUT[key] = True
            elif type_ == tmEventSetup.Charge:
                self.charge = charge_encode(cut.getData())
    def _init_external(self, handle):
        """Handle external object specific attributes."""
        # External objects only
        if handle.getType() == tmEventSetup.EXT:
            self.ext_signal_name = handle.getExternalSignalName()
            self.ext_channel_id = handle.getExternalChannelId()
        else:
            self.ext_signal_name = None
            self.ext_channel_id = None

class ConditionHelper(object):
    CombCondition = 'comb_cond'
    ExtCondition = 'ext_cond'
    Types = {
        tmEventSetup.SingleEgamma: CombCondition,
        tmEventSetup.DoubleEgamma: CombCondition,
        tmEventSetup.TripleEgamma: CombCondition,
        tmEventSetup.QuadEgamma: CombCondition,
        tmEventSetup.SingleJet: CombCondition,
        tmEventSetup.DoubleJet: CombCondition,
        tmEventSetup.TripleJet: CombCondition,
        tmEventSetup.QuadJet: CombCondition,
        tmEventSetup.SingleTau: CombCondition,
        tmEventSetup.DoubleTau: CombCondition,
        tmEventSetup.TripleTau: CombCondition,
        tmEventSetup.QuadTau: CombCondition,
        tmEventSetup.SingleMuon: CombCondition,
        tmEventSetup.DoubleMuon: CombCondition,
        tmEventSetup.TripleMuon: CombCondition,
        tmEventSetup.QuadMuon: CombCondition,
        tmEventSetup.Externals: ExtCondition,
    }
    def __init__(self, handle):
        self.name = filters.generic.snakecase(handle.getName())
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
        self.name = filters.generic.snakecase(handle.getName())
        self.expression = self.__format_expr(handle.getExpressionInCondition())
    def __format_expr(self, expr):
        # replace operators
        for k,v in self.Operators.iteritems():
            expr = re.sub(r'([\)\(\s])({})([\(\s])'.format(k), r'\1{}\3'.format(v), expr)
        # replace condition names
        def condition_rename(match):
            name = filters.generic.snakecase(match.group(1))
            return "{}.{}".format(self.condition_namespace, name)
        expr = re.sub(r'([\w_]+_i\d+)', condition_rename, expr)
        return expr

CustomFilters = {
    'c_hex': filters.hls.hex,
    'c_init_list': filters.hls.init_list,
    'hex': filters.vhdl.hex,
    'hexstr': filters.vhdl.hexstr,
    'hexuuid': filters.vhdl.hexuuid,
    'vhdl_bool': filters.vhdl.boolean,
    'mmhashn': filters.generic.murmurhash,
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
