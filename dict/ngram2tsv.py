#!/usr/bin/python
# encoding: utf-8
# Created on 7 Apr 2008 Mamoru Komachi <mamoru-k@is.naist.jp>
# ngram2kkm.py [list of ngram.gz]

import gzip
import sys
import re
from optparse import OptionParser

def main():
  """Parsed Google N-gram Format
#       words   freq
word    csv
word    csv
EOS
  """
  parser = OptionParser()
  (opts, args) = parser.parse_args()

  hiragana = re.compile(u"[\u3041-\u3093]")
  katakana = re.compile(u"[\u30a1-\u30f4]")
  def is_hiragana(string):
    return hiragana.search(string) is not None
  def is_katakana(string):
    return katakana.search(string) is not None

  #dict = {}
  re_header = re.compile("^#\t.*\t[0-9]+$")

  for f in args:
    try:
      fp = gzip.open(f, 'r')
      freq = 0
      word = ''
      read = ''
      for line in fp.readlines():
        if re_header.match(line):
          header = line.split('\t')
          # hash is not escaped!
          try:
            freq = header[2].rstrip()
          except IndexError, e:
            sys.stderr.write( "Cannot assign index %s:%s\n" % (line, e) )
            sys.exit(-1)
        elif line == 'EOS\n':
          freq = 0
        else: # morph
          tsv = line.split('\t')
          word = tsv[0]
          try:
            csv = tsv[1].split(',')
          except IndexError, e:
            sys.stderr.write("Cannot assign line %s %s:%s" % (line, tsv, e))
            sys.exit(-1)
          if len(csv) <= 7:
            if is_katakana(word.decode('utf-8')):
              read = word
            else:
              # doesn't seem to estimate reading
              continue
          else:
            read = csv[7]
          key = "%s\t%s\t%s" % (word, read, freq)
          print key
    except IOError, e:
      sys.stderr.write("Cannot open file %s:%s" % (f, e))
      sys.exit(-1)

if __name__ == "__main__":
  main()
