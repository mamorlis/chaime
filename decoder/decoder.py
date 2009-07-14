#!/usr/bin/python
# Created on 22 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import math

class Node:
  def __init__(self, length=0, endpos=0, cost=0, word=''):
    self.length = length
    self.endpos = endpos
    self.cost   = cost
    self.word   = word
    self.next   = False
    self.gn     = 0
    self.fn     = sys.maxint

  def __cmp__(self, other):
    return cmp(self.fn, other.fn)

class Decoder:
  def __init__(self, slm, kkm, dict):
    self.unk_cost = int(math.log(sys.maxint) * 2 ** 12)
    self.slm = slm
    self.kkm = kkm
    self.dict = dict
    self.alpha  = 0.9 # linear interpolation, how much you trust bigram

  def forward_search(self, sentence):
    """Returns DP path"""
    bos = Node(word="<S>")
    nodes = { 0:{ "<S>":bos } }
    usentence = sentence.decode('utf-8')

    for i in range(len(usentence)):
      for j in range(i + 1, len(usentence) + 1):
        read = usentence[i:j].encode('utf-8')
        words = self.dict.lookup(read)
        for word in words:
          cur_node = Node(length=j-i, endpos=j, word=word)
          if nodes.has_key(i):
            cost_min = sys.maxint
            kkm_cost = self.kkm.get_cost(word, read)
            for (prev_word, prev_node) in nodes[i].iteritems():
              if kkm_cost == -1:   # unknown word
                cur_cost = self.unk_cost * cur_node.length
              else:
                cur_cost = self.alpha * self.slm.get_bigram_cost(word, prev_word) \
                         + (1 - self.alpha) * self.slm.get_unigram_cost(word) \
                         + kkm_cost
              cost = prev_node.cost + cur_cost
              if cost_min > cost:
                cost_min = cost
            cur_node.cost = cost_min
          if not nodes.has_key(j):
            nodes[j] = { word:cur_node }
          elif nodes[j].has_key(word):
            if nodes[j][word].cost > cur_node.cost:
              nodes[j][word] = cur_node
          else:
            nodes[j][word] = cur_node
    return nodes

  def nbest_search(self, sentence, nbest, wordbreak):
    """Forward DP and backward A* search algorithm."""
    nbest_sentences = {}
    nbest_generator = self.astar_search(self.forward_search(sentence), sentence)
    for (converted, cost) in nbest_generator:
      if wordbreak:
        converted = " ".join(converted)
      else:
        converted = "".join(converted)
      if not nbest_sentences.has_key(converted):
        nbest_sentences[converted] = cost
      elif nbest_sentences[converted] > cost:
        nbest_sentences[converted] = cost
      if len(nbest_sentences) == nbest:
        break
    return nbest_sentences.items()

  def astar_search(self, nodes, sentence):
    """Forward Viterbi and backward A* search algorithm"""
    from pqueue import PriorityQueue
    open_list = PriorityQueue(0)
    
    eos = Node(word='</S>', endpos=len(nodes)-1)
    open_list.put((eos.cost, eos))

    while not open_list.empty():
      cur_cost, cur_node = open_list.get()
      if cur_node.word == '<S>':
        read = [ ]
        node = cur_node
        while node.next:
          node = node.next
          read.append(node.word)
          if node.word == '<S>':
            raise(StopIteration)
        read.pop()  # </S>
        yield (read, cur_node.fn)
        while not open_list.empty():
          cur_cost, cur_node = open_list.get()
          if cur_node.word != '<S>':
            break
      # backward probability estimation
      for backward_node in nodes[cur_node.endpos - cur_node.length].values():
        path_cost = self.alpha * self.slm.get_bigram_cost(cur_node.word,
                                             backward_node.word)
        backward_node.gn = path_cost + cur_node.gn
        backward_node.fn = path_cost + cur_node.gn + backward_node.cost \
             + (1 - self.alpha) * self.slm.get_unigram_cost(backward_node.word)
        backward_node.next = cur_node
        open_list.put((backward_node.fn, backward_node))
