#!/usr/bin/python
# Created on 18 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

from hira2kata import hira2kata
import pytc

class KKM:
  """Kana-Kanji Modeling"""
  def __init__(self, trans_table):
    # construct translation table
    self.dict = pytc.BDB(trans_table, pytc.BDBOREADER)

  def get_cost(self, word, read):
    """Looks up probability of a given word"""
    if self.dict.has_key(word):
      katakana = hira2kata(read)
      for cand_cost in self.dict.getlist(word):
        cand, cost = cand_cost.split()
        if cand == katakana:
          return int(cost)
    # not found
    return -1
