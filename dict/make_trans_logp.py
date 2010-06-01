#!/usr/bin/python
# encoding: utf-8
# Created on 25 Mar 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math
from optparse import OptionParser

def main():
  scaling = 2 ** 12

  for line in sys.stdin:
    line = line.rstrip()
    (word, yomi, prob) = line.split()
    cost = int(scaling * -math.log(float(prob)))
    print "%s %s %s" % (word, yomi, cost)

if __name__ == "__main__":
  main()
