#!/usr/bin/python
# Created on 18 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

from hira2kata import hira2kata
import pytc
try:
  set
except NameError:
  from sets import Set as set

class JDIC():
  """Looks up a dictionary"""
  def __init__(self, dict):
    self.dict = self.set_dict(dict)

  def set_dict(self, dict):
    """Loads TokyoCabinet"""
    tcb = pytc.BDB(dict, pytc.BDBOREADER)
    return tcb

  def get_dict(self):
    """Returns dictionary object"""
    return self.dict

  def lookup(self, read):
    """Looks up a dictionary given reading"""
    katakana = hira2kata(read)
    surfaces = set()
    surfaces.add(read)
    surfaces.add(katakana)
    if self.get_dict().has_key(read):
      for word in self.get_dict().getlist(read):
        surfaces.add(word)
    return surfaces
