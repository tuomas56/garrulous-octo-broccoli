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

```python
>>> import main
>>> html = """<div></div>"""
>>> css = """*{ display: block; padding: 10px; background: #ff0000; }"""
>>> width, height = 1000, 1000
>>> main.render_to_file(html, css, width, height, "outfile.ppm")
```
