from __main__ import app
from requests import get
from urllib import parse
from flask import request, render_template, redirect

# static pages handling
@app.route('/', methods=["GET"])
def home_load():
  return render_template('index.html')

@app.route('/search', methods=["GET"])
def search_page():
	if not request.args['q']:
		return 'Error', 400
	elif len(request.args['q']) == 0:
		return 'Error', 400
	elif request.args['q'].startswith('!'):
		query = parse.quote(request.args['q'])
		data = get(f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1")
		parsed = data.json()
		return redirect(parsed['Redirect'], code=301)
	else:
		return render_template('search.html', query=request.args['q'])

@app.route('/search/images', methods=["GET"])
def images_page():
	if not request.args['q']:
		return 'Error', 400
	elif len(request.args['q']) == 0:
		return 'Error', 400
	else:
		return render_template('images.html', query=request.args['q'])