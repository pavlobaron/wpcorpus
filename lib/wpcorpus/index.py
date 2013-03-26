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

from rabbit import Consumer
from props import Props
import pickle
from tables import *

BASE_PATH = "/Users/pb/code/wpcorpus"

class IndexEntry(IsDescription):
    cat = StringCol(255)
    filename = StringCol(255)
    start = UInt64Col()
    length = UInt32Col()

class Index(object):
    group = None
    table = None
    entry = None

    def __init__(self):
        self.filename = "%s/corpus/ix/h5.ix" % BASE_PATH
        self.open_ix(create = True)

        self.p = Props()
        self.p.backpressure = 100
        self.p.exchange = "wikiindex"
        self.queue = Consumer(self.p)

    def open_ix(self, create = False):
        self.h5 = openFile(self.filename, mode = "a", title = "Wiki Index")
        if create:
            self.group = self.h5.createGroup("/", 'index', 'Wiki Index')
            self.table = self.h5.createTable(self.group, 'index', IndexEntry, "Wiki Index")
        else:
            self.group = self.h5.root.index
            self.table = self.h5.root.index.index

        self.entry = self.table.row

    def consume(self):
        self.queue.start(self.on_message, self.p.exchange)

    def on_message(self, message):
        msg = pickle.loads(message)
        if type(msg) == tuple:
            cat, filename, start, end = msg

            print cat

            for c in cat:
                self.entry['cat'] = c.encode('ascii', "ignore")
                self.entry['filename'] = filename.encode("ascii", "ignore")
                self.entry['start'] = start
                self.entry['length'] = end
                self.entry.append()
                print c
        else:
            self.h5.close()
            self.open_ix()

if __name__ == "__main__":
    i = Index()
    i.consume()
