class Node: pass

class Text(Node):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value

class Element(Node):
	def __init__(self, tag_name, attributes, children):
		self.tag_name = tag_name
		self.attributes = attributes
		self.children = children

	def get(self, name):
		for attr in self.attributes:
			if attr.name == name:
				return attr.value

	def __str__(self):
		return "<%s %s> %s </%s>" % (self.tag_name, ' '.join(map(str, 
			self.attributes)), ' '.join(map(str, self.children)), self.tag_name)

class Attribute:
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __str__(self):
		return "%s=%s" % (self.name, self.value)