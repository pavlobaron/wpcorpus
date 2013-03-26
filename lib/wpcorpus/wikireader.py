#
# This file is part of wpcorpus
#
# Copyright (c) 2013 by Pavlo Baron (pb at pbit dot org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *
import nltk.data
from nltk.tokenize import *
from tables import *
from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *

DELIM = "----"
DELIM2 = "|"
IRR = "irr"

class CategorizedWikiCorpusReader(object):
    def __init__(self, root, fileids, cat_pattern=""):
        self.ix = "%s/ix/h5.ix" % root
        catpat = cat_pattern.pattern.split(DELIM)
        self.cat = catpat[0]
        self.yescats = catpat[1].split(DELIM2)
        self.nocats = catpat[2].split(DELIM2)
        self.tokenizer = WordPunctTokenizer()
        self.h5 = openFile(self.ix)
        self.table = self.h5.root.index.index

    def categories(self):
        return [self.cat, IRR]

    def fileids(self, categories):
        if categories[0] == self.cat:
            cats = self.yescats
        else:
            cats = self.nocats

        rows = []
        for cat in cats:

            print "training %s as %s" % (cat, categories[0])

            sk = 'cat == "%s"' % cat
            for r in self.table.where(sk):
                rows.append("%s%s%s%s%s" %
                            (r['filename'],
                             DELIM,
                             r['start'],
                             DELIM,
                             r['length']))

        return rows

    def words(self, fileids=None):
        words = []
        for fid in fileids:
            row = fid.split(DELIM)
            f = open(row[0])
            f.seek(int(row[1]), 0)
            text = f.read(int(row[2]))
            f.close()

            words.extend(self.tokenizer.tokenize(text))

        return words
