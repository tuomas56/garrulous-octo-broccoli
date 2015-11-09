#!/usr/bin/env python3

import html, css, style, layout, painting, dom
import argparse
import sys

def renderer_string_to_class(s):
	if s == 'ppm':
		return painting.PPMRenderer

def render_to_image(html_source, css_source, height, width, renderer):
	tree = html.parse(html_source)
	rules = css.parse(css_source)

	styled_tree = style.style(tree, rules)

	layout_tree = [layout.build_layout_tree(node) for node in styled_tree if layout.get_display(node) is not layout.Display.NONE]

	root = layout.Dimensions.default()
	root.content.width = width

	for node in layout_tree:
		node.layout(root)

	renderer = renderer_string_to_class(renderer)(height, width)
	image = renderer.render(layout_tree)

	return image

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('--html', default='', help='html source to render.')
	parser.add_argument('--css', default='', help='css to style html with.')
	parser.add_argument('--renderer', default='ppm', help='renderer to use: ppm, svg, tkinter')
	parser.add_argument('--height', default=1000, type=int, help='height of output document.')
	parser.add_argument('--width', default=1000, type=int, help='width of output document.')
	parser.add_argument('--out', default=None, help='file to save output to.')
	args = parser.parse_args(argv[1:])

	image = render_to_image(args.html, args.css, args.height, args.width, args.renderer)

	if args.out is not None:
		with open(args.out, "w") as f:
			image.dump(f)

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
