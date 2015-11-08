from css import *
import functools

class LayoutBox:
	def __init__(self, node, dimensions, children):
		self.node = node
		self.dimensions = dimensions
		self.children = children

class BlockNode(LayoutBox):
	def layout(self, containing_block):
		self.calculate_block_width(containing_block)
		self.calculate_block_position(containing_block)
		self.layout_block_children()
		self.calculate_block_height()

	def calculate_block_width(self, containing_block):
		auto = Keyword("auto")
		width = self.node.get("width") or auto

		zero = Length(0.0, Unit.PX)

		margin_left = self.node.get("margin-left", "margin") or zero
		margin_right = self.node.get("margin-right", "margin") or zero
		border_left = self.node.get("border-left", "border") or zero
		border_right = self.node.get("border-right", "border") or zero
		padding_left = self.node.get("padding-left", "padding") or zero
		padding_right = self.node.get("padding-right", "padding") or zero

		total = [margin_left, margin_right, border_left,
				 border_right, padding_left, padding_right]
		total = sum([x.value for x in total if x != auto])

		if width != auto and total > containing_block.content.width.value:
			if margin_left == auto:
				margin_left = zero
			if margin_right == auto:
				margin_right = zero

		underflow = containing_block.content.width - total

		if width != auto and margin_left != auto and margin_right != auto:
			margin_right = Length(margin_right.value + underflow, Unit.PX)
		elif width != auto and margin_left != auto and margin_right == auto:
			margin_right = Length(underflow, Unit.PX)
		elif width != auto and margin_left == auto and margin_right != auto:
			margin_left = Length(underflow, Unit.PX)
		elif width == auto:
			if margin_left == auto:
				margin_left = zero
			if margin_right == auto:
				margin_right = zero

			if underflow >= 0.0:
				width = Length(underflow, Unit.PX)
			else:
				width = zero
				margin_right = Length(margin_right.value + underflow, Unit.PX)
		elif width != auto and margin_left == auto and margin_right == auto:
			margin_left = Length(underflow / 2.0, Unit.PX)
			margin_right = Length(underflow / 2.0, Unit.PX)

		self.dimensions.content.width = width.value
		self.dimensions.margin.left = margin_left.value
		self.dimensions.margin.right = margin_right.value
		self.dimensions.border.left = border_left.value
		self.dimensions.border.right = border_right.value
		self.dimensions.padding.left = padding_left.value
		self.dimensions.padding.right = padding_right.value

	def calculate_block_position(self, containing_block):
		d = self.dimensions

		zero = Length(0.0, Unit.PX)
		auto = Keyword('auto')

		d.margin.top = self.node.get("margin-top", "margin") or zero
		d.margin.top = zero if d.margin.top == auto else d.margin.top
		d.margin.top = d.margin.top.value

		d.margin.bottom = self.node.get("margin-bottom", "margin") or zero
		d.margin.bottom = zero if d.margin.bottom == auto else d.margin.bottom
		d.margin.bottom = d.margin.bottom.value

		d.border.top = self.node.get("border-top", "border") or zero
		d.border.top = zero if d.border.top == auto else d.border.top
		d.border.top = d.border.top.value
		d.border.bottom = self.node.get("border-bottom", "border") or zero
		d.border.bottom = zero if d.border.bottom == auto else d.border.bottom
		d.border.bottom = d.border.bottom.value

		d.padding.top = self.node.get("padding-top", "padding") or zero
		d.padding.top = zero if d.padding.top == auto else d.padding.top
		d.padding.top = d.padding.top.value
		d.padding.bottom = self.node.get("padding-bottom", "padding") or zero
		d.padding.bottom = zero if d.padding.bottom == auto else d.padding.bottom
		d.padding.bottom = d.padding.bottom.value

		d.content.x = containing_block.content.x + d.margin.left + d.border.left
		d.content.x += d.padding.left

		d.content.y = containing_block.content.height + containing_block.content.y
		d.content.y += d.margin.top + d.border.top + d.padding.top

	def layout_block_children(self):
		d = self.dimensions
		for child in self.children:
			child.layout(d)
			d.content.height += child.dimensions.margin_box().height

	def calculate_block_height(self):
		height = self.node.get("height")
		if isinstance(height, Length):
			self.dimensions.content.height = height.value

class InlineNode(LayoutBox): pass

class AnonymousBlock(LayoutBox):
	def __init__(self, dimensions, children):
		self.dimensions = dimensions
		self.children = children

class Rect:
	def __init__(self, x, y, width, height):
		self.x, self.y = x, y
		self.width, self.height = width, height

	def expanded_by(self, edge):
		return Rect(self.x - edge.left, self.y - edge.top,
			self.width + edge.left + edge.right,
			self.height + edge.top + edge.bottom)

	@staticmethod
	def default():
		return Rect(0, 0, 0, 0)

class EdgeSizes:
	def __init__(self, left, right, top, bottom):
		self.left, self.right = left, right
		self.top, self.bottom = top, bottom

	@staticmethod
	def default():
		return EdgeSizes(0, 0, 0, 0)

class Dimensions:
	def __init__(self, content, padding, border, margin):
		self.content = content
		self.padding = padding
		self.border = border
		self.margin = margin

	@staticmethod
	def default():
		return Dimensions(Rect.default(), EdgeSizes.default(), 
			EdgeSizes.default(), EdgeSizes.default())

	def padding_box(self):
		return self.content.expanded_by(self.padding)

	def border_box(self):
		return self.padding_box().expanded_by(self.border)

	def margin_box(self):
		return self.border_box().expanded_by(self.margin)

class Display:
	BLOCK = 0
	INLINE = 1
	NONE = 2

def get_display(node):
	display = node.get('display')
	display = display if display is not None else Keyword('inline')
	if display.value == 'inline':
		return Display.INLINE
	elif display.value == 'block':
		return Display.BLOCK
	elif display.value == 'none':
		return Display.NONE

def build_layout_tree(node):
	display = get_display(node)
	if display is Display.NONE:
		raise RuntimeError("Root node has display: none!")
	elif display is Display.INLINE:
		root = InlineNode(node, Dimensions.default(), [])
	elif display is Display.BLOCK:
		root = BlockNode(node, Dimensions.default(), [])

	for child in root.node.children:
		display = get_display(child)
		if display is Display.NONE:
			continue
		elif display is Display.INLINE:
			get_inline_container(root).children.append(
				build_layout_tree(child))
		elif display is Display.BLOCK:
			root.children.append(build_layout_tree(child))

	return root

def get_inline_container(root):
	if isinstance(root, (InlineNode, AnonymousBlock)):
		return root
	elif isinstance(root, BlockNode):
		if isinstance(root.children[-1], AnonymousBlock):
			return root.children[-1]
		else:
			root.children.append(AnonymousBlock(
				Dimensions.default(), []))
			return root.children[-1]