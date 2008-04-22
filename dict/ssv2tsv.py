#!/usr/bin/python
# created on 4 April 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys,os

def main():
  import re
  hira = re.compile(r'^(?:\xE3\x81[\x81-\xBF]|\xE3\x82[\x80-\x93])+$')
  for line in sys.stdin.readlines():
    fields = line.split()
    m = hira.search(fields[0])
    if m != None:
      # all hiragana
      continue
    print "\t".join(fields)

if __name__ == "__main__":
  main()
