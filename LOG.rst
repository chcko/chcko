===
LOG
===


20191203
========

https://github.com/mamchecker/mamchecker
is built on Python2 because Google was late to adopt Python3.

Now *google appengine* has become *google cloud platform* and Python3 is supported.
Moreover 3rd party libraries don't need to be part of the app tree.
The app tree can rather be seen as Python3 package and 3rd party libraries
listed in ``requirements.txt`` will be installed automatically.

This necessitates changes almost equivalent to a rewrite.

I Made a *new organization* to hold the python 3 version of mamchecker:
https://github.com/chcko.
Due to limited time, it will take possibly a year to complete the changes.
Luckily Goople continues to support Python2 apps.
So mamchecker stays online.
Content can be added to mamchecker.
I can be moved to chcko when chcko is completed.


