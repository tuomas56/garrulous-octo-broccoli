#!/usr/bin/env python3

import tkinter
import tkinter.filedialog
import gui
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

def main(url=''):
	top = gui.Tk(title='Browser', set_minsize=True)
	html, css = '', ''
	curl = tkinter.StringVar(value=url)
	history = [curl.get()]
	index = 0
	def do_new_window():
		main()

	def do_go_button():
		nonlocal index
		history.insert(index + 1, curl.get())
		index += 1
		do_reload()

	def do_reload():
		nonlocal html, css, curl
		html, css = networking.get_page(history[index]).decode(), ''
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
		image = m.render_to_image(html, css, canvas.get().winfo_height(), canvas.get().winfo_width(), CanvasImage)
		canvas.get().delete("all")
		image.dump(canvas.get())

	def do_open():
		nonlocal curl
		filename = tkinter.filedialog.askopenfilename(title="Open a file", filetypes=(("Html files", "*.html"), ("All files", "*.*")))
		curl.set("file://" + filename)
		do_go_button()

	def do_save():
		file = tkinter.filedialog.asksaveasfile(title="Save file as", filetypes=(("Html files", "*.html"), ("All files", "*.*")))
		file.write("<style>%s</style>%s" % (css, html))
		file.close()

	def do_back():
		nonlocal index
		if index > 0:
			index -= 1
			do_reload()

	def do_forward():
		nonlocal index
		if index < (len(history) - 1):
			index += 1
			do_reload()

	canvas = gui.Canvas(width=500, height=500, pack_expand=True, pack_fill='both')
	top << canvas

	address = gui.Entry(textvariable=curl, pack_expand=True, pack_fill='x')

	with gui.frame(top, pack_fill='x') as f:
		f << gui.Button(command=do_back, text="<-")
		f << gui.Button(command=do_forward, text="->")
		f << address
		f << gui.Button(command=do_go_button, text="Go", pack_side='right')

	menu = gui.Menu(tearoff=False)
	filemenu = gui.Menu(tearoff=False)
	viewmenu = gui.Menu(tearoff=False)

	top << menu
	menu << filemenu
	menu << viewmenu

	menu.get().add_cascade(label="File", menu=filemenu.get())
	menu.get().add_cascade(label="View", menu=viewmenu.get())

	viewmenu.get().add_command(label="Reload", command=do_reload)

	filemenu.get().add_command(label="New Window", command=do_new_window)
	filemenu.get().add_command(label="Open File", command=do_open)
	filemenu.get().add_command(label="Save", command=do_save)

	top.get().configure(menu=menu.get())

	canvas.get().bind("<Configure>", do_resize)
	canvas.get().bind("<Key>", do_key)
	canvas.get().bind("<Button-1>", do_left_mouse)
	canvas.get().bind("<Button-2>", do_right_mouse)
	canvas.get().bind("<Enter>", do_mouse_enter)
	canvas.get().bind("<Leave>", do_mouse_leave)
	do_reload()
	top.mainloop()

if __name__ == "__main__":
	main(sys.argv[1] if len(sys.argv) == 2 else '')