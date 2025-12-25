#!/usr/bin/env python3
import requests
import socket
import argparse

names = [ "home", "jellyfin" ]

def set_ipv6_address(ip, name, key):
    url = f"https://api.gandi.net/v5/livedns/domains/welsby.de/records/{name}/AAAA"
    payload = "{\"rrset_values\":[\"" + ip + "\"],\"rrset_ttl\":320}"
    headers = {
        "authorization": f"Bearer {key}",
        "content-type": "application/json"
    }
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response.text


def get_current_ipv6():
    try:
        return socket.getaddrinfo("home.welsby.de", None, socket.AF_INET6)[0][4][0]
    except:
        return None


def get_new_ipv6():
    """Get the current external IPv6 address or return None if no connection to the IPify service is possible"""
    try:
        return requests.get("https://api6.ipify.org", timeout=5).text
    except requests.exceptions.ConnectionError as ex:
        return None


def main():
    parser = argparse.ArgumentParser(
                    prog='dynip',
                    description='Set AAAA record to current ipv6 address')
    parser.add_argument('-k', '--key')
    args = parser.parse_args()

    cur_ip = get_current_ipv6()

    if cur_ip is None:
        print("Failed to get current IP address")
        return

    new_ip = get_new_ipv6()

    if new_ip is None:
        print("Failed to get new IP address")
        return

    if cur_ip != new_ip:
        print(f"Current IP: {cur_ip}")
        print(f"New IP: {new_ip}")

        for name in names:
            print(f"Setting IP address for {name}")
            result = set_ipv6_address(new_ip, name, args.key)
            print(f"Result: {result}")


if __name__ == "__main__":
    main()
