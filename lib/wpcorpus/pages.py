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

from lxml.etree import iterparse
import re

def extract_page(xmlf):
    i = iterparse(xmlf)
    tag = i.next()
    title = ""
    while tag:
        if tag[0] == 'end':
            if tag[1].tag.endswith("title"):
                title = tag[1].text
            elif tag[1].tag.endswith("text"):
                yield (title, tag[1].text)
                title = ""
    
        tag = i.next()

patterns = [
            [re.compile("\*+", re.M), ""], #asterisks
            [re.compile("'+", re.M), ""], #font format
            [re.compile(":\s", re.M), ""], #indentations
            [re.compile("#\s", re.M), ""], #numbered lists

            [re.compile("<[^<>]+?>", re.M), " "], #any xml/html tags
            [re.compile("<[^<>]+?>", re.M), " "], #any xml/html tags (nested)
            [re.compile("{{[^{}]*?}}", re.M), ""], #anything within {{}}
            [re.compile("{{[^{}]*?}}", re.M), ""], #anything within {{}} (nested)
            [re.compile("=+\s*(See also|External links|References|Other representations)\s*=+", re.M), ""], #noise headings
            [re.compile("#REDIRECT\s+\[\[.*?\]\]", re.M), ""], #redirects
            [re.compile("http://[\w/.\-]+", re.M), ""], #http references
            [re.compile("\[\[[^\[\]]*?\|\s*([^\|\[]*?)\s*\]\]", re.M), r"\1"], #internal links
            [re.compile("\[\[[^\[\]]+?\]\]", re.M), ""], #anything within [[]]
            [re.compile("\[\[[^\[\]]+?\]\]", re.M), ""], #anything within [[]] (nested)
            [re.compile("\[[^\[\]]+?\]", re.M), ""], #anything within []

            #table
            [re.compile("{\|[^\n]*?\n", re.M), ""], #start
            [re.compile("\|}", re.M), ""], #end
            [re.compile("\|\+([^\n]*)\n", re.M), r"\1"], #caption
            [re.compile("\|-[^\n]*\n", re.M), "\n"], #splitter
            [re.compile("([^!])!([^!]*)!!", re.M), r"\1!\n\2!"], #headers reformat
            [re.compile("!\s*([^!\n]+)\n", re.M), r"\1\n"], #headers (multi liner)
            [re.compile("([^\|])\|([^\|]*)\|\|", re.M), r"\1\|\n\2\|"], #row reformat
            [re.compile("\|\s*([^\|\n]*)\n", re.M), r"\1\n"], #row (multi liner)

            [re.compile("{[^{}]*?}", re.M), ""], #anything within {}
            [re.compile("----", re.M), ""], #rule
            [re.compile("=+\s*(.+?)\s*=+", re.M), r"\n\1\n"], #headings
            [re.compile("&[^;\s]+?;", re.M), " "], #html special chars

            [re.compile("\s*\(\s*\)\s*", re.M), " "], #rest noise
            [re.compile("\s*\[\s*\]\s*", re.M), " "], #rest noise
            [re.compile("(\s*,\s*)+", re.M), ", "], #rest noise
            [re.compile("(\s*\.\s*)+", re.M), ". "], #rest noise
            [re.compile("\s*\|\s*", re.M), ""], #rest noise
            [re.compile("\n\n+", re.M), "\n"], #multi LF
            [re.compile("\s\s+", re.M), " "] #multi spaces
        ]

def filter_markup(page):
    text = page
    for a in patterns:
        text = re.sub(a[0], a[1], text)

    text = text.strip()

    return text

def clean_title(title):
    return re.sub(re.compile("|.*"), "", title)

def extract_cat(page):
    cat = re.findall(re.compile("\[\[Category:(.*?)\]\]"), page)
    cat = [re.sub(re.compile("^(.*?)\|.*$"), r"\1", c).strip() for c in cat]
    cat = [c for c in cat if len(c) > 0]

    return cat

def extract_text(xmlf):
    for title, page in extract_page(xmlf):
        if page:
            title = clean_title(title)
            cat = extract_cat(page)
            if title and len(title) > 0 and cat and len(cat) > 0:
                text = filter_markup(page)
                yield (cat, title, text)
