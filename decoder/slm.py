#!/usr/bin/python
# Created on 18 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math
import pytc

class SLM:
  """Statistical Language Modeling"""
  def __init__(self, slm):
    self.bigram = pytc.BDB(slm, pytc.BDBOREADER)
    self.bigram_cache = {}

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
      return sys.maxint
