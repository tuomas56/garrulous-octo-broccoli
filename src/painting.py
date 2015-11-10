from layout import *

class PPMImage:
	def __init__(self, width, height):
		self.pixels = [(255, 255, 255)]*(width*height)
		self.height = height
		self.width = width

	def set_pixel(self, x, y, color):
		self.pixels[int(x) + int(y)*self.width] = color

	def get_pixel(self, x, y):
		return self.pixels[int(x) + int(y)*self.width]

	def draw_pixel(self, x, y, color):
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			self.set_pixel(x, y, color)

	def draw_rect(self, x, y, width, height, color):
		for dx in range(int(width)):
			for dy in range(int(height)):
				self.draw_pixel(x + dx, y + dy, color)

	def dump(self, file):
		file.write("P3\n")
		file.write("%s %s\n" % (self.width, self.height))
		file.write("255\n")
		for y in range(self.height):
			row_string = []
			for x in range(self.width):
				row_string.append("%s %s %s" % tuple([str(x).rjust(3, ' ') for x in self.get_pixel(x, y)]))
			file.write(' '.join(row_string) + '\n')

class SVGImage:
	def __init__(self, width, height):
		self.width, self.height = width, height
		self.rects = []

	def draw_rect(self, x, y, width, height, color):
		self.rects.append((x, y, width, height, color))

	def dump(self, file):
		file.write('<svg width="%s" height="%s">' % (self.width, self.height))
		for x, y, width, height, color in self.rects:
			file.write('<rect x="%s" y="%s" width="%s" height="%s" style="stroke:none;fill:#%.2x%.2x%.2x;" />' % 
				(x, y, width, height, color[0], color[1], color[2]))
		file.write('</svg>')

class Renderer:
	def __init__(self, width, height, image):
		self.image = image(width, height)

	def render_background(self, cmd_list, node):
		file = self.image
		if isinstance(node, (InlineNode, BlockNode)):
			bb = node.dimensions.border_box()
			background = node.node.get('background')
			if not background:
				return
			cmd_list.append((file.draw_rect, bb.x, bb.y, bb.width, bb.height, background.to_tuple()))


	def render_border(self, cmd_list, node):
		file = self.image
		if isinstance(node, (InlineNode, BlockNode)):
			d = node.dimensions
			bb = d.border_box()
			color = node.node.get('border-color')
			if color is None:
				return
			cmd_list.append((file.draw_rect, bb.x, bb.y, d.border.left, bb.height, color))
			cmd_list.append((file.draw_rect, bb.x + bb.width - d.border.right, bb.y, d.border.right, bb.height, color))
			cmd_list.append((file.draw_rect, bb.x, bb.y, bb.width, d.border.top, color))
			cmd_list.append((file.draw_rect, bb.x, bb.y + bb.height - d.border.bottom, bb.width, d.border.bottom, color))

	def render_image(self, cmd_list, node):
		pass

	def render_box(self, root, cmd_list):
		self.render_background(cmd_list, root)
		self.render_border(cmd_list, root)

		if root.node.node.tag_name == "img":
			self.render_image(cmd_list, root)

		for child in root.children:
			render_box(child, cmd_list, image)

	def render(self, nodes):
		cmd_list = []

		for node in nodes:
			self.render_box(node, cmd_list)

		for func, *args in cmd_list:
			func(*args)

		return self.image