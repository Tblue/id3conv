#!/usr/bin/env python2
#
# Converts ID3 tags in a file to ID3 v2.3.0.

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