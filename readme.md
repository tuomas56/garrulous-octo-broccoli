#garrulous-octo-broccoli

A HTML & CSS parser and rendering engine implemented in Python.
Following the tutorial by Matt Brubeck on [his website.](http://limpet.net/mbrubeck/2014/08/08/toy-layout-engine-1.html)

##Dependencies

* *funcparserlib*

##Currently Supports

* Output to PPM P3 and SVG formats.
* Block rendering.
* Background and border colours.
* Inline stylesheets in *style* elements.
* Simple Tkinter based browser.
* Simple networking with *http* and *file* url schemes.

##Usage

###Rendering

As API:

```python
>>> import main
>>> html = """<div></div>"""
>>> css = """*{ display: block; padding: 10px; background: #ff0000; }"""
>>> width, height = 1000, 1000
>>> main.render_to_file(html, css, width, height, "outfile.ppm")
```

From CLI:

```
usage: main.py [-h] [--html HTML] [--css CSS] [--renderer RENDERER]
               [--height HEIGHT] [--width WIDTH] [--out OUT]

optional arguments:
  -h, --help           show this help message and exit
  --html HTML          html source file to render.
  --css CSS            css file to style html with.
  --renderer RENDERER  renderer to use: ppm, svg, tkinter
  --height HEIGHT      height of output document.
  --width WIDTH        width of output document.
  --out OUT            file to save output to.
```

###Browser

As API:

```python
>>> import browse
>>> browse.main(input('enter a url: '))
```

From CLI:

```
usage: browse.py [url]

optional arguments:
	url				   url to display.
```
