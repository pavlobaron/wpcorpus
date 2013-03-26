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

import os

BASE_PATH = "/Users/pb/code/wpcorpus"
DUMP_FILE = "enwiki-20121201-pages-articles.xml"
CHUNK_SIZE = 64000000
STEP_SIZE = 1024
START = "<mediawiki>"
END = "</mediawiki>"

def main():
    fin = open("%s/dump/%s" % (BASE_PATH, DUMP_FILE), "r")
    chunk = 1
    rest = None
    stop = False
    while not stop:
        fout = open("%s/dump/chunk/%s.xml" % (BASE_PATH, chunk), "w")
        if chunk > 1:
            fout.write(START)

        if rest:
            fout.write(rest)
            rest = None

        for i in range(0, CHUNK_SIZE / STEP_SIZE):
            buf = fin.read(STEP_SIZE)
            if buf and len(buf) > 0:
                fout.write(buf)
            else:
                stop = True

        while not stop:
            l = fin.readline()
            if l:
                tmpl = l.strip()
                if tmpl.startswith("</page"):
                    fout.write(l)
                    l = fin.readline()
                    tmpl = l.strip()
                    if not tmpl.startswith(END):
                        rest = l
                        fout.write(END)
                    else:
                        stop = True
                        fout.write(l)

                    break
                else:
                    fout.write(l)
            else:
                break

        fout.close()
        chunk += 1

    fin.close()

if __name__ == '__main__':
    main()
