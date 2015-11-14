import urllib.request
import urllib.parse
import os.path

def get_page(url):
	scheme, server, path, *_ = urllib.parse.urlparse(url)
	if scheme == 'http':
		return retrieve_http(scheme + '://' + server + path), ''
	elif scheme == 'file':
		return retrieve_file(server + path), ''

def retrieve_http(url):
	return urllib.request.urlopen(url).read()

def retrieve_file(filename):
	with open(os.path.expanduser(filename), "r") as f:
		return f.read()