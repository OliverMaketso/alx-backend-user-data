#!/usr/bin/python3
""" Check response
"""
import requests

if __name__ == "__main__":
    r = requests.get('http://0.0.0.0:5000/api/v1/forbidden/')
    if r.status_code != 403:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
   
    print("OK", end="")
