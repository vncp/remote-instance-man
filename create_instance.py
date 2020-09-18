#!/usr/bin/env python3
import argparse
import logging
import pathlib
import subprocess
import sys
import os
import re
import create_vnc_unit
import pexpect
import set_vncpasswd
import time

parser = argparse.ArgumentParser(description='Goes through process of adding the instance')
parser.add_argument('--units_dir', type=str, help='Directory of unit files', default="units")
parser.add_argument('--netid', type=str, help='NetID')
parser.add_argument('--template', type=str, help="Unit template file", default="templates/vnc-unitfile.tmpl")

NS_DATABASE = "nis"

#Logging Setup
LOG_FORMAT = '%(message)s' 
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

def main(args):
    # Create the unit file
    port_num = create_vnc_unit.main(args)
    print(f"create_instance got {args.netid}")
    # Generate random password
    passwd = set_vncpasswd.get_random_alphaNumeric_string()
    #Set VNC password and restart the service file
    print(f"Password: {passwd}")

    process = pexpect.spawn(f'su {args.netid}')
    process.sendline('vncpasswd')
    process.expect('Password:', timeout=4)
    process.sendline(passwd)
    process.expect('Verify:', timeout=4)
    process.sendline(passwd)
    process.expect('Would you like to enter a view-only password (y/n)?', timeout=4)
    process.sendline('n')
     
    result = os.system(f'systemctl restart vnc-{args.netid}-{port_num}.service')
    if os.WEXITSTATUS(result) == 0:
        logging.info(f"Restarted vnc-{args.netid}-{port_num}.service")
    else:
        logging.warning(f"Failed to restart vnc-{args.netid}-{port_num}.service")
        return 2

    return 0

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
 
