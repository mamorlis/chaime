#!/usr/bin/python
# Created on 18 Feb 2008 Mamoru Komachi <mamoru-k@is.naist.jp>

import sys
import slm
import kkm
import dict
import decoder
from optparse import OptionParser

class ChaIME:
  """Term-based Yet Another Input Method Editor"""
  def __init__(self, config):
    self.slm     = slm.SLM(config.get('dict', 'unigram'),
                           config.get('dict', 'bigram'))
    self.kkm     = kkm.KKM(config.get('dict', 'kkm'))
    self.dict    = dict.JDIC(config.get('dict', 'word'))
    self.decoder = decoder.Decoder(self.slm, self.kkm, self.dict)
    self.version = '0.2.6'

def main():
  parser = OptionParser()
  parser.add_option("-v", "--version", dest="version",
                    action="store_true", default=False,
                    help="Returns version string")
  parser.add_option("-i", "--ini", dest="ini",
                    help="Ini file")
  parser.add_option("-n", "--nbest", dest="nbest",
                    help="N-best search (default 1)")
  parser.add_option("-d", "--debug", dest="debug",
                    action="store_true", default=False,
                    help="Debug")
  parser.add_option("-w", "--wordbreak", dest="wordbreak",
                    action="store_true", default=False,
                    help="Put word separator between words")
  parser.add_option("-j", "--ajaxime", dest="ajaxime",
                    action="store_true", default=False,
                    help="Output in AjaxIME format")
  parser.add_option("-s", "--skk", dest="skk",
                    action="store_true", default=False,
                    help="Run in skkserv mode")
  (opts, args) = parser.parse_args()

  import ConfigParser
  config = ConfigParser.SafeConfigParser()
  if opts.ini:
    config.read(opts.ini)
  else:
    import os.path
    config.read(os.path.dirname(sys.argv[0]) + '/chaime.ini')
  chaime = ChaIME(config)

  if opts.version:
    print chaime.version
    sys.stdout.flush()
    sys.exit(0)

  while True:
    nbest = int(opts.nbest) if opts.nbest else 1
    try:
      line = raw_input().lstrip()
    except EOFError:
      break

    if opts.skk:
      try:
        mode = int(line[0])
      except ValueError, e:
        sys.stderr.write("Protocol must be an integer:\n%s\n" % (e))
        sys.exit(-1)
      except IndexError, e:
        sys.stderr.write("Protocol must start from an integer:\n%s\n" % (e))
        sys.exit(-1)

      # parse skk protocol
      if mode == 0:
        return 0
        break
      elif mode == 1:
        line = line.decode("euc-jp").encode("utf-8")
        index = line.find(" ")
        if index != -1:
          line = line[1:index]
        else:
          print "4 "
          sys.stdout.flush()
          continue
      elif mode == 2:
        print "chaime-%s " % (chaime.version)
        sys.stdout.flush()
        continue
      elif mode == 3:
        import socket
        fqdn = socket.getfqdn()
        print "%s:%s: " % (fqdn, socket.gethostbyname(fqdn))
        sys.stdout.flush()
        continue
      else:
        print "0 "
        sys.stdout.flush()
        continue

    sys.stdout.flush()
    if len(line) > 0:
      nbest_sentences = chaime.decoder.nbest_search(line, nbest, opts.wordbreak)
      nbest_sentences.sort(lambda x,y: cmp(x[1],y[1]))
      if opts.ajaxime:
        print "ImeRequestCallback([%s]);" \
          % (",".join(["'" + x + "'" for x,y in nbest_sentences]))
      elif opts.skk:
        if nbest_sentences[0] != line:
          print "1/%s/" \
            % ("/".join([x.decode('utf-8').encode('euc-jp') for x,y in nbest_sentences]))
        else:
          print "4%s" % (line)
      else:
        for (sentence, cost) in nbest_sentences:
          if opts.debug:
            print "%s (cost:%s)" % (sentence, cost)
          print sentence
      sys.stdout.flush()
  return 0

if __name__ == "__main__":
  main()
