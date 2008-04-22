#!/usr/bin/python
# Created on 09 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
from optparse import OptionParser

def main(kana, fp):
  words       = {}
  input_words = {}
  for line in fp.readlines():
    (word, read, freq) = line.split()
    if kana:
      (word, read) = (read, word)   # need kana-kanji table
    if len(word) < 1 or len(read) < 1 or freq < 1:
      continue
    input = (word, read)
    input_words[input] = input_words.get(input, 0) + int(freq)
    words[word] = words.get(word, 0) + int(freq)
  for input in input_words.iteritems():
    print input[0][0], input[0][1], \
        float(input[1]) / float(words[input[0][0]])

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-k", "--kana", dest="kana", action="store_true",
                    default=False,
                    help="Contsruct Kana to Kanji table")
  (opts, args) = parser.parse_args()
  main(opts.kana, sys.stdin)
