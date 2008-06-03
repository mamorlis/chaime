#!/usr/bin/python
# encoding: utf-8
# Created on 7 Apr 2008 Mamoru Komachi <mamoru-k@is.naist.jp>
# ngram2kkm.py [list of ngram.gz]

import MeCab
import sys
from optparse import OptionParser

def main():
  try:
    t = MeCab.Tagger("-p")
  except RuntimeError, e:
    sys.stderr.write("Cannot exec MeCab:%s\n" % (e))
    sys.exit(-1)
  kkm_table = {}
  for f in sys.argv[1:]:
    try:
      fp = open(f, 'r')
      for line in fp.xreadlines():
        line = line.rstrip()
        (ngram, freq) = line.split("\t")
        partial = [ x + "\t*" for x in ngram.split(" ") ]
        partial.append("EOS\n")
        m = t.parseToNode("\n".join(partial))
        while m:
          csv = m.feature.split(",")
          if len(csv) >= 8:
            reading = csv[7]
            if m.surface != '' and reading != '*':
              kkm_table[(m.surface, reading)] = freq
          m = m.next
      sys.stderr.write("Read %s\n" % (f))
    except IOError, e:
      sys.stderr.write("Cannot open file %s:%s" % (f, e))
      sys.exit(-1)
  for (word, keys) in kkm_table.iteritems():
    print "%s\t%s\t%s" % (word[0], word[1], keys)

if __name__ == "__main__":
  main()
