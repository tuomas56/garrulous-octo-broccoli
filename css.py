from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import *
import functools


token_specs = [
	('LBR', ("{",)),
	('RBR', ("}",)),
	('NUMBER', ("-?[0-9]+(\.[0-9]+)?",)),
	('COLON', (":",)),
	('DOT', ("\.",)),
	('HASH', ("#",)),
	('SEMI', (";",)),
	('TEXT', ('[^{}:\.#; \t\n]+',)),
	('WS', ("[ \t\n]+",))
]

tokenizer = make_tokenizer(token_specs)
tokenize = lambda s: list(tokenizer(s))

class Rule:
	def __init__(self, selector, declarations):
		self.selector = selector
		self.declarations = declarations

	def matches(self, element):
		return self.selector.matches(element)

	def specificity(self):
		return self.selector.specificity()

	def defines(self, name):
		return name in [d.name for d in self.declarations]

	def get(self, name):
		return [d for d in self.declarations if d.name == name][0].value

class Selector:
	def __init__(self, tag_name, id_name, class_names):
		self.tag_name = tag_name
		self.id_name = id_name
		self.class_names = class_names

	def specificity(self):
		return (self.tag_name != '*') + (self.id_name is not None) + (
			len(self.class_names))

	def matches(self, element):
		if self.tag_name != element.tag_name and self.tag_name != '*':
			return False
		if self.id_name is not None and self.id_name != element.get('id'):
			return False
		if not all((cls in element.get('class').split()) for cls in self.class_names):
			return False
		return True

class Declaration:
	def __init__(self, name, value):
		self.name = name
		self.value = value

def parse_value(value, values):
	result = []
	values.insert(0, value)
	for value in values:
		if isinstance(value, str):
			result.append(Keyword(value))
		elif isinstance(value, tuple):
			if value[0].type == 'HASH':
				result.append(Color(value[1]))
			elif value[0].type == 'NUMBER':
				result.append(Length(value[0].value, value[1]))
	return result[0] if len(result) == 1 else result

class Color:
	def __init__(self, val):
		val = ''.join([x.value if isinstance(x, Token) else x for x in val])

		self.r = int(val[:2], 16)
		self.g = int(val[2:4], 16)
		self.b = int(val[4:], 16)

	def to_tuple(self):
		return (self.r, self.g, self.b)

class Length:
	def __init__(self, val, unit):
		self.value = float(val)
		self.unit = parse_unit(unit)

	def __add__(self, other):
		return Length(self.value + other.value, self.unit)

	def __sub__(self, other):
		return Length(self.value - other.value, self.unit)

	@staticmethod
	def default():
		return Length(0, Unit.PX)

class Keyword:
	def __init__(self, value):
		self.value = value

	def __eq__(self, other):
		return self.value == other.value

class Unit:
	PX = 1

def parse_unit(val):
	if val == 'px':
		return Unit.PX

def starred(func):
	@functools.wraps(func)
	def _starred(args):
		return func(*args)
	return _starred

toktype = lambda s: some(lambda t: t.type == s)
tok = lambda typ, val: some(lambda t: t.type == typ and t.value == val)
lbr = toktype('LBR')
rbr = toktype('RBR')
number = toktype('NUMBER')
colon = toktype('COLON')
text = toktype('TEXT') >> (lambda t: t.value)
ws = toktype('WS')
dot = toktype('DOT')
semi = toktype('SEMI')
hash_ = toktype('HASH')

class_selector = skip(dot) + text
id_selector = skip(hash_) + text
simple_selector = text + maybe(id_selector) + many(class_selector)

selector = simple_selector >> starred(Selector)

unit = text
keyword = text
length = number + unit
color = hash_ + oneplus(number | text)
value = (keyword | length >> tuple | color >> tuple) + many(keyword | length | color) >> starred(parse_value)

declaration = text + skip(colon) + value >> starred(Declaration)

rule = selector + skip(lbr) + many(declaration + skip(semi)) + skip(rbr)
rule >>= starred(Rule)

toplevel = many(rule) + skip(finished)

parse = lambda s: toplevel.parse([x for x in tokenize(s) if x.type != 'WS'])
