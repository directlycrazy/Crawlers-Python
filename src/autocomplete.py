from __main__ import app
from urllib import parse
from flask import request, jsonify
from requests import get

@app.route('/autocomplete', methods=["GET"])
def autocomplete():
	if not request.args['q']:
		return 'Error', 400
	elif len(request.args['q']) == 0:
		return 'Error', 400
	query = parse.quote(request.args['q'])
	resp = get(f'https://suggestqueries.google.com/complete/search?client=firefox&q={query}')
	res = [request.args['q'],resp.json()[1]]
	return jsonify(res)