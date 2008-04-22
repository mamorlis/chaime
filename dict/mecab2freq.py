#!/usr/bin/python
# Created on 09 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys,os

if __name__ == "__main__":
  freq_of = {}
  for line in sys.stdin.readlines():
    if line.startswith("EOS"): continue
    fields = line.split("\t")
    input = (fields[0], fields[1])
    freq_of[input] = freq_of.get(input, 0) + 1
  for input in freq_of.iteritems():
    print input[0][0], input[0][1], input[1]
