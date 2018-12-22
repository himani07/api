import flask
from flask import request, jsonify
import pandas as pd
import json
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#generate csv with random values
import numpy as np
np.random.seed(0) 
k=1
N=1000
dataframe = pd.DataFrame({ 'B' : np.random.randint(k, k + 500 , size=N),'A' : range(1545295826000, N +1545295826000 ,1)})
dataframe.to_csv('data.csv', index=False,header=False)


#Read data from csv
df = pd.read_csv("data.csv", header=None)
df.columns = ['post_id', 'timestamp']
df = df.to_json(orient='records')
posts=json.loads(df)
#print(posts)

'''
posts = [
    {"post_id":5,"timestamp":"1545295826000"},
	{"post_id":5,"timestamp":"1545295826001"},
	{"post_id":5,"timestamp":"1545295826002"},
	{"post_id":4,"timestamp":"1545295828000"}
]
'''

@app.route('/', methods=['GET'])
def home():
    return '''<h1>API for fetching unique posts based on timestamp</p>'''


@app.route('/get_data/all', methods=['GET'])
def api_all():
    return jsonify(posts)


@app.route('/get_data/', methods=['GET'])
def api_id():
	if 'page' in request.args:
		post_id = int(request.args['page'])
	else:
		return "Error: No id field provided. Please specify an id."
	results = []
	for post in posts:
		if post['post_id'] == post_id:
			results.append(post)
	results=sorted(results, key=lambda k: k['timestamp'],reverse=True) 
	results=next(iter(results))
	return jsonify(results)

app.run()