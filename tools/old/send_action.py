#!/usr/bin/env python3
import sys, json, requests

if len(sys.argv) < 3:
    print("Usage: ./send_json.py <file_name> <url>")
    exit(1)
    
try:
    send_file = open(sys.argv[1], "r")
except FileNotFoundError:
    print("File not found")
    exit(1)

data = json.load(send_file)

url = "http://" + sys.argv[2] + "/action"
if url[:7] == url[7:14]:    # Remove extra https:// if it exists
    url = url[7:]
print("Url:",url)


r = requests.post(url, json=data)

