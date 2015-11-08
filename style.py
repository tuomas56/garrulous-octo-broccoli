from css import *
from dom import *

MULTIPLE_ORDER = ["left", "right", "top", "bottom"]

class StyledNode(Node):
	def __init__(self, node, rules, children):
		self.node = node
		self.rules = rules
		self.children = children

	def get(self, name, alternate=None):
		for rule in self.rules:
			if rule.defines(name):
				return rule.get(name)
		if alternate is not None:
			for rule in self.rules:
				if rule.defines(alternate):
					if isinstance(rule.get(alternate), list):
						return rule.get(alternate)[MULTIPLE_ORDER.index(name.split("-")[1])]
					else:
						return rule.get(alternate)

def get_rules(e, stylesheet):
	return sorted([x for x in stylesheet if x.matches(e)],
			key=lambda x: x.specificity(), reverse=True)

def style(tree, stylesheet):
	result = []
	for root in tree:
		if root.tag_name == 'style':
			stext = ''.join(map(lambda x: x.value, root.children))
			stylesheet.extend(parse(stext))
			continue
		if len(root.children):
			children = style(root.children, stylesheet)
		else:
			children = []
		result.append(StyledNode(root, get_rules(root, stylesheet), children))
	return result

