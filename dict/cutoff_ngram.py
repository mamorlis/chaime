#!/usr/bin/python
# Created on 10 Apr 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import gzip
from optparse import OptionParser

def main():
  parser = OptionParser()
  parser.add_option("-v", "--vocab", dest="vocab",
                    help="Filename of a vocab file (sorted)")
  parser.add_option("-t", "--threshold", dest="thres",
                    help="Threshold parameter to cut off")
  (opts, args) = parser.parse_args()
  vocab_gz = opts.vocab if opts.vocab \
                        else "/work2/ngram/GSK2007-C/Vol1/data/1gms/vocab_cs.gz" 
  threshold = int(opts.thres) if opts.thres else 1000
                
  try:
    fp = gzip.open(vocab_gz, 'r')
    for line in fp.readlines():
      line = line.rstrip()
      (word, freq) = line.split("\t")
      if int(freq) > threshold:
        print line
      else:
        break
  except IOError, e:
    sys.stderr.write("Cannot open vocab file %s:%s\n" % (vocab_gz, e))
    sys.exit(-1)

if __name__ == "__main__":
  main()
