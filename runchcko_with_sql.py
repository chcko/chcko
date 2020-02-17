#!/usr/bin/env python

"""
./runchcko_with_sql.py gunicorn
./runchcko_with_sql.py
"""

import sys
import os
import conftest

from chcko.chcko.run import main

if __name__ == '__main__':
    try:
        main(sys.argv[1])
        exit(0)
    except:
        pass
    main(None)
