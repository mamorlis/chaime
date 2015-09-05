# ChaIME -- Term-based Yet Another Japanese Input Method Editor #

ChaIME is a Japanese input method editor based on Anthy. It aims at sophisticated unknown word detection, community-based development of dictionaries, and application of generalized language model.

## Introduction ##

In recent years, the expansion of WWW allows common users to obtain large amount of text data with little effort. People get more and more used to use computers to write documents. Compared to old word processing era, the accuracy of commercial Japanese Input Method Editors (IME) become acceptable, and one can type messages in Japanese without so much stress these days.

Contrary, open source Operating Systems such as Linux and FreeBSD stick on using outdated IMEs such as Canna and Wnn. It was only recently that high accurate free and open source IME called Anthy came into existence. Anthy has been widely used as default Japanese IME in many modern distributions, including Ubuntu, SUSE and Mandriva.

Anthy first introduced statistical language model in 2005, and then (maximum entropy-based) discriminative conversion model in 2006. However, it is based on the dictionary called cannadic, which is maintained as part of Canna, and there are many parameters and resources that need hand-tuning. The requirement of human intervention makes development of Anthy hard to maintain.

To mitigate the problem, we propose a novel Japanese IME called ChaIME (pronounced as "chime"). It is based on statistical model and can estimate co-occurrence parameters automatically. It also make use of gigantic corpora extracted from the Web to develop linguistic knowledge-free IME.

## Open Issue ##

  1. Slow translation (can be sped up by coverting system dictionaries into DFA)
  1. Distribution of the system including its language model (Google Japanese N-gram data cannot be distributed itself)
  1. Port to other platforms (SCIM, uim, Emacs)

## Acknowledgement ##

This IME is partly supported by the Creative and International Competitiveness Project 2007, Nara Institute of Science and Technology, Japan.