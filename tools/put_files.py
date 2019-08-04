#!/usr/bin/env python3

import subprocess
import tempfile
import sys

if len(sys.argv) < 2:
    print("Usage: ./put_files.py <filename>")
    exit(1)

with open(sys.argv[1], 'r') as rows:
    for row in rows:
        if row[0] == "#":
            continue
        row = row.split(',')
        if len(row) < 4:
            continue
        row = [x.strip('\n') for x in row]
        print(row)
        if row[3] == "git":
            subprocess.run(["ssh", "-i", row[0], row[1], "cd "+ row[2] + "; git stash; git pull"])
            continue
        with tempfile.NamedTemporaryFile() as tf:
            tf.write(bytes('cd ' + row[2] + '\nput -r ' + row[3] +'/* .', 'utf-8'))
            tf.flush()
            subprocess.run(["sftp", "-i", row[0], "-b", tf.name, row[1]])
