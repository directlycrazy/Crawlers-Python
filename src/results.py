import urllib.request
from __main__ import app
from flask import request, jsonify
from requests import get
from urllib import parse
from bs4 import BeautifulSoup

@app.route('/results/<func>')
def results(func):
	query = request.args['q']
	request_query = parse.quote(request.args['q'])
	if not query:
		return 'Error', 400
	if func == 'search':
		# normal google searching
		url = f'https://google.com/search?q={request_query}'
		req = urllib.request.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
		raw_response = urllib.request.urlopen(req).read()
		html = raw_response.decode("utf-8")
		soup = BeautifulSoup(html, 'html.parser')
		divs = soup.select("#search div.g")
		complete_array = []
		for div in divs:
			results = div.select("h3")
			links = div.select("a")
			descriptions = div.select('div.VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf')
			this_json = {}
			if (len(results) >= 1):
				h3 = results[0]
				if not h3 or not h3.get_text():
					this_json['title'] = ""
				else:
					this_json['title'] = h3.get_text()
			if (len(links) >= 1):
				link = links[0]
				if not link:
					this_json['link'] = ""
				elif not link.has_key('href'):
					this_json['link'] = ""
				elif link['href'].startswith("/search?q="):
					this_json['link'] = ""
				else:
					this_json['link'] = link['href']
			if (len(descriptions) >= 1):
				desc = descriptions[0]
				if not desc or not desc.get_text():
					this_json['snippet'] = ""
				else:
					this_json['snippet'] = desc.get_text()
			if this_json.get('snippet') is None:
				this_json['snippet'] = 'No additional information provided.'
			if this_json.get('snippet') and this_json.get('title') and this_json.get('link'):
				if not this_json.get('title') == 'Images':
					complete_array.append(this_json)	
		return jsonify({"results" : complete_array})
	elif func == "images":
		# image searching
		url = f'https://www.bing.com/images?q={request_query}'
		req = urllib.request.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36')
		raw_response = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(raw_response, 'html.parser')
		results = []
		for link in soup.find_all(class_ = "mimg"):
			imgurl = link.get('data-src')
			if imgurl:
				results.append({"url" : imgurl})
		return jsonify(results)
	elif func == "knowledge":
		if 'ip' in request_query and 'my' in request_query:
			return 'Server IP Address Redacted', 404
		resp = get(f'https://api.duckduckgo.com/?q={request_query}&format=json').json()
		if resp['Abstract']:
			return jsonify({
				"description" : resp['Abstract'],
				"source" : resp['AbstractSource'],
				"url" : resp['AbstractURL'],
				"heading" : resp['Heading'],
				"related" : resp['RelatedTopics'],
				"image" : resp['Image']
			})
		elif resp['Heading']:
			return jsonify({
				"source" : resp['AbstractSource'],
				"url" : resp['AbstractURL'],
				"heading" : resp['Heading'],
				"related" : resp['RelatedTopics'],
				"image" : resp['Image']
			})
		elif resp['Answer']:
			return jsonify({
				"answer" : resp['Answer'],
				"answer_type" : resp['AnswerType'],
				"related" : resp['RelatedTopics'],
				"image" : resp['Image']
			})
	return 'Not Found', 404

@app.route('/results/search/pages', methods=["GET"])
def ddg_crawl():
	query = request.args['q']
	request_query = parse.quote(request.args['q'])
	if not query:
		return 'Error', 400
	else:
		if not request.args['r']:
			return 'Error', 400
		else:
			if not request.args['r'].isnumeric():
				return 'Error', 400
			else:
				url = f'https://lite.duckduckgo.com/lite/?q={request_query}'
				req = urllib.request.Request(url)
				req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
				raw_response = urllib.request.urlopen(req).read()
				html = raw_response.decode("utf-8")
				soup = BeautifulSoup(html, 'html.parser')
				results = soup.select('.result-link')
				descriptions = soup.select('.result-snippet')
				return_results = []
				i = 0
				for result in results:
					if result:
						if result.get_text():
							if result['href']:
								desc = ""
								try:
									desc = descriptions[i].get_text()
								except IndexError:
									desc = 'No additional information provided.'
								return_results.append({"title" : result.get_text(), "link" : result['href'], "snippet" : desc})
								i+=1
				return jsonify(return_results)