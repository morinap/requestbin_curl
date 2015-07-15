#!/usr/bin/python
import urllib
import json
import sys

# Client for Request Bin API
class RequestBinClient:
	api_url = ' http://requestb.in/api/v1'

	def __init__(self, api_url=''):
		if api_url != "":
			self.api_url = api_url

	# Get request info for the bin and request id
	def getRequest(self, bin_id, request_id):
		get_url = '%s/bins/%s/requests/%s' % (self.api_url, bin_id, request_id)
		f = urllib.urlopen(get_url)
		return json.loads(f.read())

# Get params
if len(sys.argv) != 3:
	print "Usage: requestbin_curl.py bin_id request_id"
	exit(1)

bin_id = sys.argv[1]
request_id = sys.argv[2]

# Create client
rb_client = RequestBinClient()
json_data = rb_client.getRequest(bin_id, request_id)

# Build CURL URL
req_url = 'http://requestb.in/%s' % (bin_id)

# Determine query string
query_string = ''
for query_key, query_value in json_data['query_string'].iteritems():
	for value in query_value:
		if query_string != '':
			query_string += '&';

		query_string += urllib.urlencode({query_key: value})

if query_string != '':
	req_url += '?%s' % (query_string)

# Init command
command = 'curl -v -X%s ' % (json_data['method'])

# Add headers
for header_name, header_value in json_data['headers'].iteritems():
	command += " -H '%s: %s'" % (header_name, header_value.replace("'", "\\'"))

command += " %s" % (req_url)

# Add body
body = json_data['body']
if body != '':
	command += " -d '%s'" % body.replace("'", "\\'")

# Output command
print "%s" % (command)