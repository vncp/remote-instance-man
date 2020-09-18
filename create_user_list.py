#!/usr/bin/env python3
import argparse
import configparser
import logging
import pathlib
import jinja2
import subprocess
import sys
import os
import re

parser = argparse.ArgumentParser(description='Adds entries to /etc/engr/vnc.yaml')
parser.add_argument('--units-dir', type=str, help='Directory of unit files')

#Logging Setup
LOG_FORMAT = '%(message)s' #Configure log message format
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG) #Use a basic config


def load_units(filepath: str):
    configs = []
    logging.debug(f"Searching ({filepath}) for systemd units.")
    cfiles = os.listdir(filepath)

    for f in cfiles:
        logging.debug(f"Found unit: ({f})")
        path = pathlib.Path(filepath, f)
        if path.is_file() is True:
            config = configparser.ConfigParser()
            config.read(path)
            configs.append(config)
        else:
            logging.debug("Not a file: {f}")

    return configs

def load_template(filepath: str) -> jinja2.Template:
    path = pathlib.Path(filepath)
    directory = str(path.parents[0])
    filename  = path.parts[-1:][0]
    logging.debug(f"Directory: {directory}")
    logging.debug(f"Filename: {filename}")
    loader = jinja2.FileSystemLoader(directory)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(filename)

    return template

def check_netid(netid: str)  -> bool:
    command = ["getent", "passwd", "-s", NS_DATABASE, netid]
    logging.debug(command)

    result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=False)

    if result.returncode == 0:
        logging.info(f"Found valid netid: {netid}")
        return True
    else:
        logging.info(f"Invalid netid: {netid}")
        return False

def get_user_port(unit_cfgs):
    logging.debug("Get user and port information")
    users_ports = {}
    for cfg in unit_cfgs:
        user_port = cfg.get('Service', 'Environment')
        logging.debug(f"User Port: {user_port}")
        matches = re.match(r"NETID=(\w+) PORT=(\d+)", user_port)
        if matches:
            user = matches.groups()[0]
            port = matches.groups()[1]
            users_ports[user] = int(port)

    return users_ports

def main(args):

    unit_cfgs = load_units(args.units_dir)

    user_port_info = get_user_port(unit_cfgs)
    for k, v in user_port_info.items():
        print(f"{k},{v}")


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

