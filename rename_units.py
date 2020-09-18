#!usr/local/env python3
import configparser
import pathlib
import re
import os


def load_units(filepath: str):
    configs = []
    cfiles = os.listdir(filepath)
    for f in cfiles:
        path = pathlib.Path(filepath, f)
        if path.is_file() is True:
            config = configparser.ConfigParser()
            config.read(path)
            configs.append(config)

    return configs


unit_cfgs = load_units("units")
users_ports = {}
for cfg in unit_cfgs:
    user_port = cfg.get('Service', 'Environment')
    matches = re.match(r"NETID=(\w+) PORT=(\d+)", user_port)
    if matches:
        user = matches.groups()[0]
        port = matches.groups()[1]
        users_ports[user] = int(port)
        print(port, user)
        if os.path.isfile(f'./units/vnc-{user}.service'):
            os.rename(f'units/vnc-{user}.service', f'units/vnc-{user}-{port}.service')
            print(f'Renaming units/vnc-{user}.service to units/vnc-{user}-{port}.service)')

