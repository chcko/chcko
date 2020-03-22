#!/usr/bin/env python

"""
./runchcko_with_sql.py gunicorn
./runchcko_with_sql.py
"""

import sys
import os

#keep this to have parallel not installed content folders in sys.path
import conftest
os.environ['CHCKOTESTING'] = "no"

from chcko.chcko.run import main

if __name__ == '__main__':
    main()
