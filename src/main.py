import html, css, style, layout, painting, dom

def render_to_file(html_source, css_source, height, width, filename):
	tree = html.parse(html_source)
	rules = css.parse(css_source)

	styled_tree = style.style(tree, rules)

	layout_tree = [layout.build_layout_tree(node) for node in styled_tree if layout.get_display(node) is not layout.Display.NONE]

	root = layout.Dimensions.default()
	root.content.width = width

	for node in layout_tree:
		node.layout(root)

	image = painting.render(layout_tree, width, height)

	with open(filename, "w") as f:
		image.dump_ppm(f)