
'''
a simple Flask example works with local (non-persistent) data store
once the service is stopped, the data will be lost

'''
from boto3 import resource
from boto3.dynamodb.conditions import Key

import dynamodb13

import random
from flask import abort,Flask, jsonify, request
app = Flask(__name__)

def AsDict(guest):
    return {'id': guest.key.id(), 'first': guest.first, 'last': guest.last}

# a list of guests

@app.route("/rest/read", methods=['GET'])
def read():
    return jsonify(dynamodb13.read_guests(dynamodb13.get_table()))

@app.route("/rest/update", methods=['PUT'])
def update():
    return jsonify(dynamodb13.update_guest(dynamodb13.get_table(), request.json['gid'], request.json['first'], request.json['last']))

@app.route("/rest/insert", methods=['POST'])
def insert():
    gid = request.json['gid']
    dynamodb13.add_guest(dynamodb13.get_table(), gid, request.json['first'], request.json['last'])
    table = dynamodb13.get_table()
    response = table.get_item(Key={'gid':gid})
    return jsonify(response['Item'])

@app.route("/rest/delete", methods=['DELETE'])
def delete():
    gid = request.json['gid']
    dynamodb13.delete_guest(dynamodb13.get_table(), gid)
    return jsonify("guest", gid, "deleted")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
