#!/usr/bin/env python3
#Takes argument of new NetID in order to add a new user using next.sh
#Reloads the instance and calls systemctl status on the new instance
import argparse
import configparser
import logging
import pathlib
import subprocess
import sys
import os
import re

parser = argparse.ArgumentParser(description='Creates a new system Daemon file for passed netID')
parser.add_argument('--N', type=str, dest='ID', nargs=1, default=" ")

#Logging Setup
LOG_FORMAT = '%(message)s' #Configure log message format
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG) #Use a basic config

def get_port():
    NAP = subprocess.Popen('./next.sh | grep -o [0-9]*', shell=True, stdout=subprocess.PIPE,)
    port_out = NAP.communicate()[0].decode('ascii').strip()
    logging.info(f"Next available port: {port_out}")
    return port_out

def check_netid(netid: str) -> bool:
    result = subprocess.run('getent passwd '+netid,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        logging.info(f"Found existing netid: {netid}")
        return True
    else:
        logging.info(f"Netid not found: {netid}")
        return False

def main(args):
    net_id = args.ID[0]
    if net_id == " ":
        logging.debug("No arguments")
        return
    
    if check_netid(net_id):
        print(f"NETID: {net_id} is already found. Will not add a new system-d file.")
        return
    else:
        next_port = get_port()
        print(f"Adding {net_id} to ./units/ on port: {next_port} ...")
        source = './units/vnc-vpham.service'
        subprocess.run(f'cp {source} ./units/vnc-{net_id}.service',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        logging.info(f"Copying system-d file from {source} to ./units/vnc-{net_id}.service")
        #Replace net-id
        subprocess.run(f"sed -i 's/vpham/{net_id}/g' ./units/vnc-{net_id}.service", stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        logging.info(f"Replacing all instances of 'vpham' with {net_id}")
        subprocess.run(f"systemctl restart vnc-{net_id}",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        subprocess.run(f"systemctl status vnc-{net_id}",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        print("Finished")

args = parser.parse_args()
main(args)
