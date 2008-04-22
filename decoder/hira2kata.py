#!/usr/bin/python
# encoding: utf-8

def katakana_value(x):
  x_num = ord(x)
  if x_num >= 0x3041 and x_num <= 0x309F:
    return unichr(ord(x) + 0x60)
  else:
    return x

def hira2kata(hira):
  """Convert Hiragana and Katakana"""
  kata = [ katakana_value(x) for x in hira.decode("utf-8") ]
  return "".join(kata).encode("utf-8")
