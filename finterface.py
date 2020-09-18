#!/usr/bin/env python3

from flask import Flask, request, json, jsonify, render_template
import create_instance
import os
import create_vnc_unit
import requests
import logging
import subprocess
import sys
import send_confirmation
from argparse import Namespace

def createNamespace(json_obj) -> Namespace:
    f_netid = json_obj.get('netid')
    f_name = json_obj.get('name')
    f_email = json_obj.get('email')
    return Namespace(netid=f_netid, name=f_name, email=f_email, units_dir="units")
    
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return "VNC Instance management - Interface"

# Returns JSON with all of the current NetIDs and their associated ports
@app.route('/query', methods = ['GET'])
def query():
    unit_cfgs = create_vnc_unit.load_units("units")
    user_port_info = create_vnc_unit.get_user_port(unit_cfgs)
    return jsonify(user_port_info), 200

@app.route('/remove', methods = ['POST'])
def remove():
    content = None
    if request.is_json:
        content = request.get_json()
    else:
        return jsonify({'code': 1000, 'description': 'Invalid JSON requests'}), 400
    args = createNamespace(content)
    cfgs = create_vnc_unit.load_units("units")
    user_port_info = create_vnc_unit.get_user_port(cfgs)
    try:
        port = user_port_info[args.netid]
    except KeyError:
        return jsonify({'code': 3000, 'description': 'No instance associated with that NetID!'})
    user_dir = f"/usr/local/etc/units/vnc-{args.netid}-{port}.service"
    if os.path.exists(user_dir):
        os.remove(user_dir)
    else:
        return jsonify({'code': 1, 'description': 'Directory not found, nothing deleted'})
    return jsonify({'code': 0, 'description': 'Successfully removed user config'})
    


@app.route('/send-confirmation', methods = ['POST'])
def sendConfirmation():
    content = None
    if request.is_json:
        content = request.get_json()
    else:
        return jsonify({'code': 1000, 'description': 'Invalid JSON requests'}), 400
    args = createNamespace(content)
    if args.netid is None or args.name is None or args.email is None:
        return jsonify({'code': 1001, 'description': 'Invalid JSON request: Missing parameters'}), 400
    send_confirmation.sendSupport(args.netid, args.name, 'e', args.email)


@app.route('/add', methods = ['POST'])
def add():
    content = None
    if request.is_json:
        content = request.get_json()
    else:
        return jsonify({'code': 1000, 'description': 'Invalid JSON request'}), 400
    args = createNamespace(content)
    if args.netid is None or args.name is None or args.email is None:
        return jsonify({'code': 1001, 'description': 'Invalid JSON request: Missing parameters'}), 400
    try:
        ret = create_instance.main(args)
    except SystemExit:
        print("Error creating an instance")
        return jsonify({'code': 1002, 'description': 'Unable to create a new instance configuration'})
    # Remove?
    if ret == 0:
        print("Successfully added")
    else:
        print(f"Failed to add {args.netid} with error code {ret}")
        return jsonify({'code':2000+ret, 'description':'Create instance failure'})
    return jsonify({'code': 0, 'description': 'Success'}), 400


if __name__ == '__main__':
    app.run(host='remote-1.engr.unr.edu')
