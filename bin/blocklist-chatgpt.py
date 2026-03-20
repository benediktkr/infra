#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import ipaddress

import requests


# https://developers.openai.com/api/docs/bots
CHATGPT_IP_LISTS={
    # OAI-SearchBot is for search. OAI-SearchBot is used to surface websites in
    # search results in ChatGPT’s search features
    # robots.txt name: OAI-SearchBot
    # Full user-agent string:
    #  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.3; +https://openai.com/searchbot
    'searchbot': 'https://openai.com/searchbot.json',

    # GPTBot is used to make our generative AI foundation models more useful
    # and safe. It is used to crawl content that may be used in training our
    # generative AI foundation models. Disallowing GPTBot indicates a site’s
    # content should not be used in training generative AI foundation models.
    # robots.txt name: GPTBot
    # Full user-agent string:
    #  Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.3; +https://openai.com/gptbot
    'gptbot' :'https://openai.com/gptbot.json',

    # When users ask ChatGPT or a CustomGPT a question, it may visit a web page
    # with a ChatGPT-User agent. ChatGPT users may also interact with external
    # applications via GPT Actions. ChatGPT-User is not used for crawling the
    # web in an automatic fashion. Because these actions are initiated by a
    # user, robots.txt rules may not apply
    # robots.txt name: ChatGPT-User
    # Full user-agent string:
    #  Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot
    'chatgpt-user': 'https://openai.com/chatgpt-user.json'

}

BLOCKLIST_D="roles/nginx/files/blocklists.d"

def make_parser():
    default_path = os.path.join(os.environ["HOME"], "infra/private", BLOCKLIST_D)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--format", default="nginx", choices=["nginx"])
    #parser.add_argument("-n", "--name", help="blocklist filename")
    parser.add_argument("-p", "--path", default=default_path, help="path to write blocklist in")
    return parser

def get_args():
    parser = make_parser()
    return parser.parse_args()

def get_iplist(iplist_name):
    url = CHATGPT_IP_LISTS[iplist_name]
    r = requests.get(url)
    r.raise_for_status()

    # j is a dict: {'creationTime': str[ISO], 'prefixes': ['ipv4Prefix': str[IP]]}
    j = r.json()

    creation_time = datetime.fromisoformat(j['creationTime'])
    prefix_count = len(j["prefixes"])
    #prefixes = {
    #    k: [item[k] for item in j['prefixes'] if k in item.keys()]
    #    for item in j['prefixes'] for k in item.keys()
    #}
    prefixes = [a['ipv4Prefix'] for a in j['prefixes']]

    print(f"IP list name: '{iplist_name}'")
    print(f"  creation time: {creation_time}")
    print(f"  count: {len(prefixes)}")
    #for item in prefixes:
    #    print(f"  prefixes ({item}): {len(prefixes[item])}")

    # TODO: sort + unique
    return prefixes


def format_ip_addr(ip_addr):
    try:
        # the ip_network function writes addresses to /32 cidr
        #   ip_network('192.168.1.1') -> 192.168.1.1/32
        #   ip_network('192.168.1.1/24') -> 192.168.1.1/24
        _ip_addr = ipaddress.ip_network(ip_addr)
        return str(_ip_addr)
    except ValueError:
        # ip_address('192.168.1.1/24') -> ValueError
        # ip_address('foo') -> ValuError
        # ip_network('foo') -> ValuError
        raise


def make_combined_iplist():
    iplists = [get_iplist(item) for item in CHATGPT_IP_LISTS]
    return [a for item in iplists for a in item]


def format_iplist(iplist, format_name):
    if format_name == "nginx":
        return [f"deny {format_ip_addr(a)};" for a in iplist]
    else:
        raise NotImplementedError(f"Format '{format_name}' is not implemented!")


if __name__ == "__main__":
    args = get_args()

    # https://developers.openai.com/api/docs/bots
    print(f"Writing blocklists to: '{args.path}'")

    #iplists = {item: get_iplist(item) for item in CHATGPT_IP_LISTS]
    for item in CHATGPT_IP_LISTS:
        iplist = get_iplist(item)
        iplist_formatted = format_iplist(iplist, args.format)
        write_filename = f"chatgpt_{item}.conf"
        write_path = os.path.join(args.path, write_filename)
        with open(write_path, 'w') as f:
            f.write('\n'.join(iplist_formatted))
        print(f"Wrote file: '{write_filename}'")

