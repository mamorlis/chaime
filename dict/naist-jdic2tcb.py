#!/usr/bin/python

import sys
import kconv

def main():
  for line in sys.stdin.xreadlines():
    line = kconv.Kata2Hira(line, kconv.EUC)
    fields = line.decode('euc-jp').split(',')
    print "%s\t%s" % (fields[11].encode('utf-8'), fields[0].encode('utf-8'))

if __name__ == "__main__":
  main()
