#!/usr/bin/env python3

import tkinter
import tkinter.filedialog
import painting
import main as m
import networking
import sys

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
	top.title("Browser")
	canvas = tkinter.Canvas(top, width=500, height=500)
	html, css = '', ''
	curl = tkinter.StringVar()
	def do_go_button():
		do_reload()

	def do_reload():
		nonlocal html, css, curl
		html, css = networking.get_page(curl.get()).decode(), ''
		do_render()

	def do_resize(event):
		do_render()

	def do_mouse_enter(event):
		do_render()

	def do_mouse_leave(event):
		do_render()

	def do_key(event):
		do_render()

	def do_left_mouse(event):
		do_render()

	def do_right_mouse(event):
		do_render()

	def do_render():
		nonlocal html, css, canvas
		image = m.render_to_image(html, css, canvas.winfo_height(), canvas.winfo_width(), CanvasImage)
		canvas.delete("all")
		image.dump(canvas)

	def do_open():
		nonlocal curl
		filename = tkinter.filedialog.askopenfilename(title="Open a file", filetypes=(("Html files", "*.html"), ("All files", "*.*")))
		curl.set("file://" + filename)
		do_reload()

	def do_save():
		file = tkinter.filedialog.asksaveasfile(title="Save file as", filetypes=(("Html files", "*.html"), ("All files", "*.*")))
		file.write("<style>%s</style>%s" % (css, html))

	frame = tkinter.Frame(top)
	menu = tkinter.Menu(top, tearoff=False)
	filemenu = tkinter.Menu(menu, tearoff=False)
	viewmenu = tkinter.Menu(menu, tearoff=False)
	menu.add_cascade(label="File", menu=filemenu)
	menu.add_cascade(label="View", menu=viewmenu)
	viewmenu.add_command(label="Reload", command=do_reload)
	filemenu.add_command(label="Open", command=do_open)
	filemenu.add_command(label="Save", command=do_save)
	top.configure(menu=menu)
	address = tkinter.Entry(frame, textvariable=curl)
	address.pack(side="left", expand=True, fill="x")
	go_button = tkinter.Button(frame, command=do_go_button, text="Go")
	go_button.pack(side="right")
	frame.pack(fill="x")
	canvas.pack(fill="both", expand=True)
	canvas.bind("<Configure>", do_resize)
	canvas.bind("<Key>", do_key)
	canvas.bind("<Button-1>", do_left_mouse)
	canvas.bind("<Button-2>", do_right_mouse)
	canvas.bind("<Enter>", do_mouse_enter)
	canvas.bind("<Leave>", do_mouse_leave)
	top.mainloop()

if __name__ == "__main__":
	main()