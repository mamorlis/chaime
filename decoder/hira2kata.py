#!/usr/bin/python
# encoding: utf-8

def hira2kata(hira):
  """Convert Hiragana and Katakana"""
  kata = [ unichr(ord(x) + 0x60) for x in hira.decode("utf-8") ]
  return "".join(kata).encode("utf-8")
