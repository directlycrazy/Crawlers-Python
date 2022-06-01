from __main__ import app
from flask import request

@app.route('/opensearch.xml', methods=["GET"])
def opensearch():
	return '''<?xml version="1.0" encoding="utf-8"?>
<OpenSearchDescription
	xmlns="http://a9.com/-/spec/opensearch/1.1/"
	xmlns:moz="http://www.mozilla.org/2006/browser/search/">
	<ShortName>Crawlers</ShortName>
	<Description>Crawl Google search results while protecting your privacy.</Description>
	<InputEncoding>UTF-8</InputEncoding>
	<Url type="text/html"  template="http://%s/search">
		<Param name="q" value="{searchTerms}"/>
	</Url>
	<Url type="application/x-suggestions+json"  template="http://%s/autocomplete">
		<Param name="q" value="{searchTerms}"/>
	</Url>
	<moz:SearchForm>http://%s/search</moz:SearchForm>
</OpenSearchDescription>''' % (request.headers.get('host'), request.headers.get('host'), request.headers.get('host')), 200, {'content-type' : 'text/xml'}