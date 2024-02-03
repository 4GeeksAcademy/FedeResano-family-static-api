"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_family_members():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int>:id', methods=['GET'])
def get_specific_member():
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        raise APIException("Member not found", status_code=404)
    

@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.json
    members = jackson_family.add_member(new_member)
    response_body = {
        "family": members
    }
    return jsonify(response_body), 201

@app.route('/members/<int>:id', methods=['DELETE'])
def delete_member():
    members = jackson_family.delete_member(id)
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int>:id', methods=['PUT'])
def update_member(id):
    updated_member = request.json
    member = jackson_family.update_member(id, updated_member)
    if member:
        return jsonify(member), 200
    else:
        raise APIException("Member not found", status_code=404)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
