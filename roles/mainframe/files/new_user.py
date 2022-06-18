#!/usr/bin/env python

from argparse import ArgumentParser
import json

import ssl

from ldap3 import Server, Connection, ALL, Tls

new_user_dn = ''

def create_user(ldap_config):
    ldap_url = ldap_config['url']
    admin_dn = ldap_config['admin_dn']
    admin_pass = ldap_config['admin_pass']

    #t = Tls(validate=ssl.CERT_REQUIRED)
    s = Server(ldap_url, use_ssl=True, port=636, get_info=ALL)   # tls=t
    with Connection(s, admin_dn, admin_pass) as c:
        c.start_tls()
        print(c.bound)
        print(c)

    # conn.add(
    #     'new_user_dn',
    #     ['inetOrgPerson', 'posixAccount'],
    #     {
    #         'cn': '',
    #         'gidNumber':'',
    #         'homeDirectory': '',
    #         'sn': '',
    #         'uid' : '',
    #         'uidNumber': '',
    #         'mail': ''
    #     }
    # )

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', default="/usr/local/etc/ldap.json")

    return parser.parse_args()

def get_config(config_path):
    with open(config_path, 'r') as f:
        return json.parse(f)


if __name__ == "__main__":
    args = get_args()
    config = get_config()

    create_user(config['ldap'])
