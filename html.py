from funcparserlib.lexer import make_tokenizer
from funcparserlib.parser import *
import funcparserlib.parser as parser
from dom import *

token_specs = [
	('LAB', ("<",)),
	('RAB', (">",)),
	('SLASH', ("\/",)),
	('EQ', ("=",)),
	('TEXT', ('[^<>\/=" \t\n]+',)),
	('STRING', ('".*?"',)),
	('WS', ("[ \t]+",)),
	('NL', ("\n",))
]

tokenizer = make_tokenizer(token_specs)
tokenize = lambda s: list(tokenizer(s))

def make_text(t):
	return Text(t.value)

def make_string(t):
	return Text(t.value[1:-1])

def make_attribute(t):
	return Attribute(t[0].value, t[1].value)

def make_tag(t):
	return Element(t[0].value, t[1], t[2])

toktype = lambda s: some(lambda t: t.type == s)
lab = toktype("LAB")
rab = toktype("RAB")
slash = toktype("SLASH")
eq = toktype("EQ")
text = toktype("TEXT") >> make_text
string = toktype("STRING") >> make_string
ws = toktype("WS")
nl = toktype("NL") >> make_text

attribute = text + skip(eq) + (string | text)
attribute >>= make_attribute

toplevel = forward_decl()

@parser.Parser
def tag(tokens, s):
	if s.pos >= len(tokens):
		raise NoParseError('no tokens left in the stream', s)
	else:
		_, s = lab.run(tokens, s)
		name, s = text.run(tokens, s)
		attributes, s = many(attribute).run(tokens, s)
		_, s = rab.run(tokens, s)

		value, s = toplevel.run(tokens, s)

		_, s = lab.run(tokens, s)
		_, s = slash.run(tokens, s)
		_, s = some(lambda t: t.value == name.value).run(tokens, s)
		_, s = rab.run(tokens, s)

		return (name, attributes, value), s

tag >>= make_tag

toplevel.define(many(text | tag | nl))

parse = lambda s: toplevel.parse([x for x in tokenize(s) if x.type != 'WS'])