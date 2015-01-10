#!/usr/bin/env python2
#
# Converts ID3 tags in a file to ID3 v2.3.0.
#
# Copyright (c) 2015, Tilman Blumenbach
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this
#    list of conditions and the following disclaimer in the documentation and/or
#    other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import mutagen
import sys

from mutagen.id3 import ID3


if len(sys.argv) < 2:
    print >> sys.stderr, "Usage:"
    print >> sys.stderr, " %s file..." % sys.argv[0]

    sys.exit(1)


for file_path in sys.argv[1:]:
    print "Loading file `%s':" % file_path,

    tags = ID3()
    try:
        tags.load(file_path, translate=False)
    except (IOError, mutagen.MutagenError) as e:
        print "ERROR: %s." % e
        continue

    if tags.version[0] == 2 and tags.version[1] == 3:
        print "OK, no conversion necessary."
        continue

    print "Converting and saving...",
    try:
        tags.update_to_v23()
        tags.save(v2_version=3)
    except (IOError, mutagen.MutagenError) as e:
        print "ERROR: %s."
        continue

    print "OK."