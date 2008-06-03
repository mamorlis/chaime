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

def hiragana_value(x):
  x_num = ord(x)
  if 0x30A1 <= x_num <= 0x30F6 or 0x30FD <= x_num <= 0x30FE:
    return unichr(ord(x) - 0x60)
  else:
    return x

def kata2hira(kata):
  """Convert Katakana and Hiragana"""
  hira = [ hiragana_value(x) for x in kata.decode("utf-8") ]
  return "".join(hira).encode("utf-8")
