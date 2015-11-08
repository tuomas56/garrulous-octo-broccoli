from layout import *

class Image:
	def __init__(self, width, height):
		self.pixels = [(0, 0, 0)]*(width*height)
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

	def dump_ppm(self, file):
		file.write("P3\n")
		file.write("%s %s\n" % (self.width, self.height))
		file.write("255\n")
		for y in range(self.height):
			row_string = []
			for x in range(self.width):
				row_string.append("%s %s %s" % tuple([str(x).rjust(3, ' ') for x in self.get_pixel(x, y)]))
			file.write(' '.join(row_string) + '\n')


def render_background(file, cmd_list, node):
	if isinstance(node, (InlineNode, BlockNode)):
		bb = node.dimensions.border_box()
		background = node.node.get('background')
		if not background:
			return
		cmd_list.append((file.draw_rect, bb.x, bb.y, bb.width, bb.height, background.to_tuple()))


def render_border(file, cmd_list, node):
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

def render_box(root, cmd_list, image):
	render_background(image, cmd_list, root)
	render_border(image, cmd_list, root)

	for child in root.children:
		render_box(child, cmd_list, image)

def render(nodes, width, height):
	image =  Image(width, height)
	cmd_list = []

	for node in nodes:
		render_box(node, cmd_list, image)

	for func, *args in cmd_list:
		func(*args)

	return image
