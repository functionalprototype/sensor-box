#!/usr/bin/env python3

# Copyright (c) 2022 Jet Townsend

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys
#import time
import csv
import time
import datetime

parser = argparse.ArgumentParser(description='parse event log')

#parser.add_argument('--event', '-e', help="description of event", default="missing")
parser.add_argument('--verbose', '-v', action='count', default=0)
#parser.add_argument('--inputfile', "-i", help="input file containing event description")
args = parser.parse_args()

# if (args.event == "missing"):
#     print("no event TODO display help")
#     exit(-1)

if (args.verbose):
    print("logging " + args.event)

#with open('bedroom-events-2023-01-06.log', 'r') as csv_file:
with open(0) as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        if (not row):
            continue
        if (row[0].startswith("description")):
            continue
        if (row[0].startswith("#") or row[1].startswith("#")):
            continue
        ts = datetime.datetime.fromtimestamp(int(row[0]))
    #        timestring = timestamp.strftime("%m-%d-%y %H:%M")
#        timestring = ""
        del row[0]
        row_out = ","
        print(ts, row_out.join(row))
    csv_file.close()
