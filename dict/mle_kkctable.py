#!/usr/bin/python
# Created on 09 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math
sys.path.append("../decoder")
from hira2kata import kata2hira

scaling = 2 ** 12

def main():
  words       = {}
  input_words = {}
  for line in sys.stdin.readlines():
    try:
      (word, read, freq) = line.split()
    except ValueError, e:
      sys.stderr.write(line)
    if len(word) < 1 or len(read) < 1 or freq < 1:
      continue
    input = (word, read)
    input_words[input] = input_words.get(input, 0) + int(freq)
    words[word] = words.get(word, 0) + int(freq)
  for input in input_words.iteritems():
    (word, read, freq) = input[0][0], input[0][1], input[1]
    prob = freq / float(words[input[0][0]])
    cost = int(scaling * -math.log(float(prob)))
    print "%s\t%s\t%s" % ( word, kata2hira(read), cost )

if __name__ == "__main__":
  main()
