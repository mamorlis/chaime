#!/usr/bin/python
# encoding: utf-8
# Created on 25 Mar 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import gzip
import math
from optparse import OptionParser

def main():
  scaling = 2 ** 12
  parser = OptionParser()
  parser.add_option("-u", "--unigram", dest="unigram", help="Unigram file")
  (opt, args) = parser.parse_args()
  if not opt.unigram:
    print "Please specify unigram file"
    sys.exit(-1)

  unigram = {}
  try:
    fp = gzip.open(opt.unigram, 'r')
    for line in fp:
      (word, count) = line.split()
      unigram[word] = int(count)
  except IOError, e:
    print "Cannot open unigram data %s" % (e)
    sys.exit(-1)
  
  for file in args:
    try:
      fp = gzip.open(file, 'r')
      for line in fp:
        (words, count) = line.split("\t")
        word = words.split()
        bigram = int(scaling * -math.log(1.0 * int(count) / unigram[word[0]]))
        print "%s\t%s" % ( words, bigram )
    except IOError, e:
      print "Cannot open bigram data %s" % (e)
      sys.exit(-1)

if __name__ == "__main__":
  main()
