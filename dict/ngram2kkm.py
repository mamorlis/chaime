#!/usr/bin/python
# encoding: utf-8
# Created on 7 Apr 2008 Mamoru Komachi <mamoru-k@is.naist.jp>
# ngram2kkm.py [list of ngram.gz]

import gzip
import pytc
import sys
from optparse import OptionParser

def main():
  """Google N-gram Format in TSV
word    read    count
EOS
  """
  parser = OptionParser()
  parser.add_option("-w", "--word", dest="word",
                    help="Filename of a word dict (tcb)")
  parser.add_option("-m", "--mle", dest="mle",
                    help="Filename of a word dict with maximum likelihood estimation (tcb)")
  (opts, args) = parser.parse_args()

  #try:
  #  words = pytc.BDB(opts.word, pytc.BDBOWRITER)
  #except:
  #  sys.stderr.write("Cannot open tcb:%s\n" % (opts.word))
  #  sys.exit(-1)
  words = {}
  try:
    mle_words = pytc.BDB(opts.mle, pytc.BDBOWRITER)
  except:
    sys.stderr.write("Cannot open tcb:%s\n" % (opts.mle))
    sys.exit(-1)

  for f in args:
    try:
      fp = gzip.open(f, 'r')
      for line in fp.readlines():
        (word, read, freq) = line.rstrip().split("\t")
        words[word] = words.get(word, '') + read + "\t" + freq + "\n"
      sys.stderr.write("Read %s\n" % (f))
    except IOError, e:
      sys.stderr.write("Cannot open file %s:%s" % (f, e))
      sys.exit(-1)
  for (word, keys) in words.iteritems():
    best_read = ''
    best_freq = 0
    total_freq = 0
    for read_freq in keys.split("\n"):
      (read, freq) = read_freq.split("\t")
      if best_freq < int(freq):
        best_freq = int(freq)
        best_read = read
      total_freq += int(freq)
    mle_words[word] = "%s %s" % (best_read, float(best_freq) / total_freq)
  mle_words.close()

if __name__ == "__main__":
  main()
