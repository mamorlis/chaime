#!/usr/bin/python
# Created on 9 Apr 2008 Mamoru Komachi <mamoru-k@is.naist.jp>
# This module is taken from
# http://mail.python.org/pipermail/python-list/2006-March/372978.html

import Queue, bisect

class PriorityQueue(Queue.Queue):
  def _put(self, item):
    bisect.insort_left(self.queue, item)
  def _init(self, maxsize=0):
    self.maxsize = maxsize
    self.queue = []
  def _get(self):
    return self.queue.pop(0)
  def top(self):
    _top = self.get()
    self.put(_top)
    return _top

if __name__ == "__main__":
  import unittest
  queue = PriorityQueue(0)
  queue.put((2, "second"))
  queue.put((1, "first"))
  queue.put((3, "third"))

  class PriorityQueueTestCase(unittest.TestCase):
    def test_queue(self):
      priority, value = queue.get()
      self.assertEquals(priority, 1)
      self.assertEquals(value, "first")
      priority, value = queue.get()
      self.assertEquals(priority, 2)
      self.assertEquals(value, "second")
      priority, value = queue.get()
      self.assertEquals(priority, 3)
      self.assertEquals(value, "third")

  unittest.main()
