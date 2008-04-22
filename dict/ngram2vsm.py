#!/usr/bin/python
# Created on 8 Apr 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import gzip
from optparse import OptionParser

def main():
  parser = OptionParser()
  parser.add_option("-v", dest="vocab",
                    help="Vocabulary file")
  parser.add_option("-d", dest="document",
                    help="File to store document vector")
  parser.add_option("-w", dest="word",
                    help="File to store word vector")
  (opts, args) = parser.parse_args()

  if not (opts.vocab and opts.document and opts.word):
    sys.stderr.write("Please specify -v, -d -w options\n")
    sys.exit(-1)

  vocab = {}
  try:
    fp = gzip.open(opts.vocab, 'r')
    for word in fp.readlines():
      words = word.rstrip().split("\t")
      vocab[words[0]] = len(vocab)
    vocab['<UNK>'] = len(vocab)
    vocab['NONE'] = len(vocab)
    sys.stderr.write("Read vocab file %s\n" % (opts.vocab))
  except IOError, e:
    sys.stderr.write("Cannot open vocab file %s:%s\n" % (opts.vocab, e))
    sys.exit(-1)
  try:
    document = open(opts.document, 'w')
  except IOError, e:
    sys.stderr.write("Cannot write to document file %s:%s\n"
        % (opts.document, e))
    sys.exit(-1)
  
  last_first_word = ''
  words_in_pattern = []
  def print_words():
    for word in words_in_pattern:
      print word,
    print
    document.write("%s\n" % (last_first_word))

  for f in args:
    try:
      fp = gzip.open(f, 'r')
      for line in fp.readlines():
        (ngram, count) = line.rstrip().split("\t")
        (first_word, second_word) = ngram.split()
        if first_word != last_first_word and last_first_word != '':
          print_words()
          words_in_pattern = []
          last_first_word = first_word
        words_in_pattern.append("%s:%s" % (vocab[second_word], count))
      fp.close()
      sys.stderr.write("Read file %s\n" % (f))
    except IOError, e:
      sys.stderr.write("Cannot open file %s:%s" % (f, e))
      sys.exit(-1)
  # output last one
  print_words()
  document.close()
  try:
    fp = open(opts.word, 'w')
    sorted_vocab = vocab.items()
    sorted_vocab.sort(lambda x,y: cmp(x[1], y[1]))
    for (vocab, id) in sorted_vocab:
      fp.write("%s\n" % (vocab))
    fp.close()
    sys.stderr.write("Wrote to word file %s:%s\n" % (opts.word))
  except IOError, e:
    sys.stderr.write("Cannot write to word file %s:%s\n" % (opts.word, e))
    sys.exit(-1)

if __name__ == "__main__":
  main()
