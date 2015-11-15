import tkinter as tk
from functools import partial, wraps
from contextlib import contextmanager

class _tkwrapper:
	def __init__(self, **kwargs):
		self._can_pack = True
		self.nargs = {}
		self.pargs = {}
		self.children = []
		for name, value in kwargs.items():
			if name.startswith('pack_'):
				self.pargs[name[5:]] = value
			else:
				self.nargs[name] = value

	def set_parent(self, parent):
		self._value = self._class(parent, **self.nargs)

	def append(self, element):
		element.set_parent(self.get())
		self.children.append(element)

	def __lshift__(self, child):
		self.append(child)
		return self

	def pack(self, **kwargs):
		for child in self.children:
			child.pack()

		if self._can_pack:
			kwargs.update(self.pargs)
			self.get().pack(**kwargs)
			self._can_pac = False

	def get(self):
		return self._value

class Button(_tkwrapper):
	_class = tk.Button

class Canvas(_tkwrapper):
	_class = tk.Canvas

class Entry(_tkwrapper):
	_class = tk.Entry

class Label(_tkwrapper):
	_class = tk.Label

class Menu(_tkwrapper):
	_class = tk.Menu

	def pack(self, **kwargs):
		pass

class Frame(_tkwrapper):
	_class = tk.Frame

class Tk:
	def __init__(self, **kwargs):
		self._minsize = False
		if 'set_minsize' in kwargs:
			self._minsize = kwargs['set_minsize']
			del kwargs['set_minsize']
		if 'title' in kwargs:
			title = kwargs['title']
			del kwargs['title']
		else:
			title = 'tk'
		self.tk = tk.Tk(**kwargs)
		self.tk.title(title)
		self.children = []

	def append(self, child):
		child.set_parent(self.tk)
		self.children.append(child)

	def __lshift__(self, child):
		self.append(child)
		return self

	def pack(self):
		for child in self.children:
			child.pack()

	def get(self):
		return self.tk

	def mainloop(self):
		self.pack()
		if self._minsize:
			self.tk.update()
			self.tk.minsize(self.tk.winfo_width(), self.tk.winfo_height())
		self.tk.mainloop()

@contextmanager
def frame(parent, **kwargs):
	f = Frame(**kwargs)
	f.set_parent(parent.get())
	f.pack()
	yield f
	for child in f.children:
		child.pack(side=tk.LEFT)

__all__ = [frame, Button, Canvas, Entry, Label, Menu, Frame, Tk]