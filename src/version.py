import json
from __main__ import app

@app.route('/version', methods=["GET"])
def version():
	vers = {'version': 'dev'}
	return json.dumps(vers)