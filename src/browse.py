import tkinter
import painting
import main

class CanvasImage(painting.Image):
	def __init__(self, width, height):
		self.width, self.height = width, height
		self.rects = []

	def draw_rect(self, x, y, width, height, color):
		self.rects.append((x, y, width, height, color))

	def dump(self, canvas):
		for x, y, width, height, (r, g, b) in self.rects:
			canvas.create_rectangle(x, y, x + width, y + height, fill="#%.2x%.2x%.2x" % (r, g, b), outline="")

def main():
	top = tkinter.Tk()
	canvas = tkinter.Canvas(top, width=500, height=500)
	def do_go_button():
		html, css = networking.get_page(address.get())
		image = main.render_to_image(html, css, 500, 500, CanvasImage)
		image.dump(canvas)
	go_button = tkinter.Button(top, command=do_go_button)
	go_button.pack(side=tkinter.RIGHT)
	address = tkinter.Entry(top)
	address.pack(side=tkinter.LEFT)
	canvas.pack()