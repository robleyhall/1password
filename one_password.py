#!/usr/bin/env python
# coding=utf-8
#
# API to wrap the 1password cli
#
# use the 1password entry title to query either complete 1password items or only the password
#
# assumes IBM as the account but can be easily modified to use any 1password account
#
# usage:
#
#    import one_password as op
#    password = op.get_password('sample')
#

import argparse
import json
import os
import subprocess
import sys


def op_get_cached_token():
    try:
        with open(os.path.expanduser("~/.op/session")) as s:
            session_key = s.read()
            return session_key
    except IOError:
        return None


def op_cache_token(session_env_var):
    try:
        with open(os.path.expanduser("~/.op/session"),"w") as s:
            s.write(session_env_var)
    except IOError as ioe:
        print("Error writing session cache: %s" % ioe)
    

def signin():
    session_env_var = op_get_cached_token()
    if session_env_var:
        os.environ["OP_SESSION_ibm"] = session_env_var
    out = subprocess.Popen("op get item none", shell=True, stderr=subprocess.PIPE).stderr.read()

    if 'You are not currently signed in' in out or 'Authentication required' in out:
        print('Logging into 1Password to get credentials')
        session_env_var = subprocess.Popen("op signin ibm --output=raw", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
        if not session_env_var:
            print("please login into the 1password site with id/password to establish the base account settings")
            sys.exit(1)
        
        op_cache_token(session_env_var)
        os.environ["OP_SESSION_ibm"] = session_env_var
    

def get_op_item(item):
    signin()
    cmdline = "op get item \"%s\"" % item

    out = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE).stdout.read()
    return out

def get_password_from_item(item):
    details = item.get('details')
    if details:
        fields = details.get('fields')
        if fields:
            password = [ f for f in fields if f.get('designation') == "password"][0].get('value')
            return password
        else:
            password = details.get('password')
            return password
        

def get_password(item_name):
    signin()
    item = get_op_item(item_name)
    if item:
        password = get_password_from_item(json.loads(item))
    else:
        password = None

    return password
        
def main(args):

    if args.get('item'):
        item = get_op_item(args.get('item'))
        print("retrieved item: %s" % item)
    elif args.get('password'):
        print(get_password(args.get('password')))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='retrieve 1password items and/or passwords')
    parser.add_argument('-i','--item', help='item to display in full', required=False)
    parser.add_argument('-p','--password', help='get password for item', required=False)
    args = vars(parser.parse_args())

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    main(args)
    



