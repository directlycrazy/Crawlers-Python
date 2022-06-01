import os
import logging
from flask import Flask, send_from_directory, cli
from pydoc import importfile
app = Flask('app')

logging.getLogger("werkzeug").disabled = True
cli.show_server_banner = lambda *args: None

@app.route('/favicon.ico', methods=["GET"])
def favicon():
	return send_from_directory('assets/img', 'crawlers_round.png')

# assets static directory
@app.route('/assets/<path:path>', methods=["GET"])
def assets(path):
	return send_from_directory('assets', path)

# routes
for i in os.listdir('src'):
	f = os.path.join('src', i)
	if os.path.isfile(f):
		module = importfile(f)

app.run(host='0.0.0.0', port=8080)