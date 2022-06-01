from __main__ import app
from flask import request
from requests import get

@app.route('/proxy', methods=["GET"])
def proxy():
	if not request.args['q']:
		return 'Error', 400
	req = get(request.args['q'], stream=True)
	if not req.headers:
		return 'Error', 500
	if not req.headers['content-type']:
		return 'Error', 500
	if 'image' in req.headers['content-type']:
		return req.content, 200, {'content-type' : req.headers['content-type'], 'content-length': req.headers['content-length']}
		#return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])
	else:
		return 'Error', 400