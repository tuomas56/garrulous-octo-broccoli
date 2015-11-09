#garrulous-octo-broccoli

A HTML & CSS parser and rendering engine implemented in Python.
Following the tutorial by Matt Brubeck on [his website.](http://limpet.net/mbrubeck/2014/08/08/toy-layout-engine-1.html)

##Dependencies

* *funcparserlib*

##Currently Supports

* Output to PPM P3 format.
* Block rendering.
* Background and border colours.
* Inline stylesheets in *style* elements.

##Usage

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
  --html HTML          html source to render.
  --css CSS            css to style html with.
  --renderer RENDERER  renderer to use: ppm, svg, tkinter
  --height HEIGHT      height of output document.
  --width WIDTH        width of output document.
  --out OUT            file to save output to.
```