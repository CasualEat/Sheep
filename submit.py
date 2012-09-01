from flask import Flask
from flask import request
from flask import make_response
import json
import pymongo
import os
import logging
from flask import g
from flask import jsonify

app = Flask(__name__)


@app.before_request
def before():
    g.c = pymongo.Connection()
    db = g.c['sheep']
    g.coll = db['people']

@app.teardown_request
def teardown(exception):
    g.c.disconnect()
@app.route('/submit',methods=['POST'])
def post_data():
    d = {}
    d['name'] = request.form['name']
    d['email'] = request.form['email']
    d['lat' ] = request.form['lat']
    d['lng' ] = request.form['lng']
    g.coll.insert(d)
    resp = make_response()
    resp.headers['Content-type'] = 'text/html'
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:60'
    resp.data = 'ok'
    return resp


@app.route('/fetch',methods=['GET'])
def send_data():
    d = {}
    cntr = 0
    for i in g.coll.find():
        del(i['_id'])
        d[cntr] = i
        cntr+=1
    response = jsonify(d)
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:60'
    return response


# from logging import FileHandler

# fil = FileHandler(os.path.join(os.path.dirname(__file__),'logme'),mode='a')
# fil.setLevel(logging.ERROR)
# app.logger.addHandler(fil)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')