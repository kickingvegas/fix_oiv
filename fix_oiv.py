#!/usr/bin/env python
#
# Copyright 2011 Yummy Melon Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import subprocess
import getopt
import glob
import shutil

helpString = """

DESCRIPTION
 patch_oiv is script to patch OIV.app to enable it on OS X 10.7 (Lion).

  -h, --help                   print help
  -v, --version                print version

EXAMPLE
  $ python patch_oiv.py
  $ sudo python patch_oiv.py

"""

usageString = "python patch_oiv.py"

class PatchOiv:
    version = '0.1'

    def __init__(self):
        self.cmdList = None

        self.oivAppPath = os.path.join('/', 'Applications', 'OIV.app', 'Contents', 'MacOS');
        self.systemJavaStub = os.path.join('/', 'System', 'Library', 'Frameworks',
                                           'JavaVM.framework', 'Resources', 'MacOS',
                                           'JavaApplicationStub');

        if (not os.path.exists(self.oivAppPath)):
            sys.stderr.write('ERROR: OIV is not installed in /Applications on this system.\n'
                             '       Please install it for this script to work.\n')
            sys.exit(1)
        
        if (not os.path.exists(self.systemJavaStub)):
            sys.stderr.write('ERROR: Cannot find required system file\n'
                             '       "%s"\n' 
                             '       This script can not work on this system.\n' %
                             self.systemJavaStub)
            sys.exit(1)

        

    def genBaseCommand(self):
        self.cmdList = []
        self.cmdList.append('cp')
        self.cmdList.append(self.systemJavaStub)
        self.cmdList.append(self.oivAppPath)
        
    def run(self, optlist, args):
        
        self.genBaseCommand()
        
        for o, i in optlist:
            if o in ('-h', '--help'):
                sys.stderr.write(usageString)
                sys.stderr.write(helpString)
                sys.exit(0)

            elif o in ('-v', '--version'):
                sys.stderr.write('%s\n' % self.version)
                sys.exit(0)

        #print ' '.join(self.cmdList)
        #sys.stdout.write('Patching OIV\n')
        returncode = subprocess.call(self.cmdList)

        if (returncode):
            sys.stdout.write('ERROR: You do not have direct permission to alter the OIV app\n'
                             '       on this system. Please run this script with sudo as follows:\n'
                             '       $ sudo python %s\n' % sys.argv[0])
        else:
            sys.stdout.write('Patch operation of OIV complete.\n')
                


if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:],
                                      'vh',
                                      ['version', 'help'])
                                       
    except getopt.error, msg:
        sys.stderr.write(msg.msg + '\n')
        sys.stderr.write(usageString)
        sys.exit(1)


    app = PatchOiv()
    app.run(optlist, args)
    
