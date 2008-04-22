#!/usr/bin/python
# encoding: utf-8
# Created on 25 Mar 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math

def main():
  scaling = 2 ** 12

  for file in sys.argv[1:]:
    try:
      fp = open(file, 'r')
      for line in fp:
        fields = line.split()
        if len(fields) != 3:
          continue
        (word, read, p) = fields[0], fields[1], fields[2]
        logp = int(scaling * -math.log(float(p)))
        print "%s %s %s" % ( word, read, logp )
    except IOError, e:
      print "Cannot open translation table %s" % (e)
      sys.exit(-1)

if __name__ == "__main__":
  main()
