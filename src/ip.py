from __main__ import app
from flask import request

@app.route('/ip', methods=["GET"])
def ip_return():
	return request.remote_addr