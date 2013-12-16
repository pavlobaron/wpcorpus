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

from argparse import ArgumentParser
from simpleconfigparser import simpleconfigparser as SimpleConfigParser

class Props(SimpleConfigParser):
    def expand_config(self):
        self.read(self.conf)

def proc_arg(default_conf):
    parser = ArgumentParser(description='wpcorpus')
    parser.add_argument('-c', metavar='CONF', default=default_conf,
                        type=str, dest='conf', help='Configuration file')
    parser.add_argument('-v', '--version', action='version',
                        version='0.1', help="prints the current program version")

    props = Props()
    parser.parse_args(namespace=props)
    props.expand_config()

    return props
