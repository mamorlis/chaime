#!/usr/bin/python
# Created on 18 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math
import pytc

class SLM:
  """Statistical Language Modeling"""
  def __init__(self, unigram, bigram_filename):
    if bigram_filename.endswith("tch"):
      self.bigram = pytc.HDB(bigram_filename, pytc.HDBOREADER)
    else:
      self.bigram = pytc.BDB(bigram_filename, pytc.BDBOREADER)
    self.bigram_cache = {}
    self.unigram = pytc.BDB(unigram, pytc.BDBOREADER)
    self.unigram_cache = {}
    self.unknown_cost = int(math.log(sys.maxint) * 2 ** 12)

  def get_bigram_cost(self, cur_word, prev_word):
    """Returns an absolute value of logarithm of a bigram probability"""
    key  = "%s %s" % (prev_word, cur_word)
    runk = "%s %s" % (prev_word, '<UNK>')
    lunk = "%s %s" % ('<UNK>', cur_word)
    if self.bigram_cache.has_key(key): return self.bigram_cache[key]

    if self.bigram.has_key(key):
      self.bigram_cache[key] = int(self.bigram[key])
      return self.bigram_cache[key]
    elif self.bigram.has_key(runk):
      self.bigram_cache[runk] = int(self.bigram[runk]) * len(cur_word)
      return self.bigram_cache[runk]
    elif self.bigram.has_key(lunk):
      self.bigram_cache[lunk] = int(self.bigram[lunk]) * len(prev_word)
      return self.bigram_cache[lunk]
    else:
      #self.bigram_cache[key] = int(self.bigram['<UNK> <UNK>']) \
      #                       * (len(cur_word) + len(prev_word))
      #return self.bigram_cache[key]
      return self.unknown_cost

  def get_unigram_cost(self, word):
    """Returns the cost of a given word"""
    if not self.unigram_cache.has_key(word):
      if self.unigram.has_key(word):
        self.unigram_cache[word] = int(self.unigram[word])
      else:
        #self.unigram_cache[word] = int(self.unigram['<UNK>']) * len(word)
        return self.unknown_cost
    return self.unigram_cache[word]
