#!/usr/bin/python
# Created on 18 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math
from hira2kata import hira2kata
import pytc

class KKM:
  """Kana-Kanji Modeling"""
  def __init__(self, trans_table):
    # construct translation table
    self.dict = pytc.BDB(trans_table, pytc.BDBOREADER)
    # memoize
    self.cand_of = {}
    self.cost_of = {}
    self.unk_cost = math.log(sys.maxint) * 2 ** 12

  def lookup_best_candidate(self, word):
    """Looks up best candidate in the dictionary"""
    # momoize
    if self.cand_of.has_key(word): return self.cand_of[word]

    if self.dict.has_key(word):
      (read, cost) = self.dict[word].split()
    else:
      cost = self.unk_cost
      read = '<UNK>'
    self.cand_of[word] = (cost, read)
    return self.cand_of[word]

  def get_cost(self, word, read):
    """Looks up probability of a given word"""
    if self.dict.has_key(word):
      katakana = hira2kata(read)
      (cost, best_read) = self.lookup_best_candidate(word)
      if best_read == katakana:
        return int(cost)
    # not found
    return -1
