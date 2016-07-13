import requests
import json
import time
import urllib
import sys

'''
Example Invocation:
$ python ols_in_efo.py [file with list of URLs] [ontology (efo, ordo, etc)] >[output file]
Before loading into PostgreSQL remove embedded double quotes with this sed:
$ sed 's/\\"//g' [ouput file] >[cleaned output file]
Loading OLS output to a transit Pg table:
$ psql -h localhost -d cttv_core_test -p 5432 -U tvdev
In psql execute COPY command:
cttv_core_test=# \COPY cttv012_variation.transit_tmp  FROM orphanet_not_in_efo_ordo_ols_json_cleaned.txt  WITH DELIMITER E'\b'
SQL To extract columns and convert the JSON output in 2nd column to JSONB:
SELECT
  (STRING_TO_ARRAY(data_row, E'\t'))[1] disease_url,
  (STRING_TO_ARRAY(data_row, E'\t'))[2]::JSONB ols_output
FROM
  cttv012_variation.transit_tmp;
'''

url_list_file = sys.argv[1]
ontology = sys.argv[2]
#http://www.ebi.ac.uk/ols/api/ontologies/efo/terms/http%253A%252F%252Fwww.orpha.net%252FORDO%252FOrphanet_1306
def get_url_list(file_path):
	'''
	Return the contents of a single column file of Ontology URLs as a list.
	'''
	url_list = [url.strip() for url in open(file_path, 'rt').read().split('\n') if len(url.strip()) > 0]
	return url_list
url_list = get_url_list(url_list_file) #['http://www.orpha.net/ORDO/Orphanet_1306', 'http://www.orpha.net/ORDO/Orphanet_1520']
for url in url_list:
	url_escaped = urllib.quote(urllib.quote(url, safe=''), safe='') # double escape!
	#print url_escaped
	time.sleep(0.1)
	#test_term = 'http%253A%252F%252Fwww.orpha.net%252FORDO%252FOrphanet_1306'
	request_url = 'http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % (ontology, url_escaped)
	req = requests.get(request_url, headers={ "Content-Type" : "application/json"})
	json_obj = req.json()
	print url + '\t' + json.dumps(json_obj)

