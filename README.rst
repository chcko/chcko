chcko
=====

Educational problem server at

    https://chcko.eu

developed at

    https://github.com/chcko/chcko

with example content package

    https://github.com/chcko/chcko-r

``chcko`` wants to collect problems,
usable by students with or without learn coaches around the world.
An infrastructure.

``chcko`` makes it easy to compose a problem set for students,
it checks the answers and gives the results.

The focus is on collecting science problems
not about code or format.

The problem packages are python packages.
the whole system can be installed locally too.

URL
===

Pages are requested with this URL format::

    ../<lang>/<page>?<query>

Pages are:

- ``org``: add roles and choose a color
- ``contents``: specific content items or overview if no ``query``
- ``done``: done problems
- ``todo``: assigned problems
- some additional helper pages

Example URLs:

| https://chcko.eu/en/org?School=S&Field=F&Teacher=T&Class=C&Role=-------
| https://chcko.eu/en/contents?r.a&r.bu
| https://chcko.eu/en/contents?r.a&&r.bu
| https://chcko.eu/en/done?*&*

With ``&&`` instead of one ``&`` as separator in a *contents* query, is called a **course**, here.
In a course only one problem at a time is shown.
``&&&`` marks the current position.
For example, ``.../en/contents?r.bd&&r.ba&&&r.a`` has ``r.a`` as current item in the course.

The names ``School, Field, Teacher, Class, Role``
form namespaces levels to describe a student *role*.
What string is used in each level is up to the user.

The namespaces are of organizational nature.
The namepace names are taken from usual organizational structures.

See `queries`_ for details.

Use Cases
=========

No Login
--------

Without login a random ``Role`` is generated.
One can revisit the ``Role`` later via the URL, for example

  https://chcko.eu/en/done?School=7f277b84&Field=8084&Teacher=5ab4&Class=87b5&Role=459671edc836

With ``Org`` one can choose names.
One can choose names via the URL, too.
For example:

  https://chcko.eu/en/org?School=noschool&Field=2020&Teacher=noteacher&Class=noclass&Role=me

Without login these names, random or not, are not protected.
Their ownership changes to a logged-in user when accessed,
either via ``Org`` or via URL.

Step-by-step try in class without logging in:

- Agree on a common ID for School, Field, Teacher and Class and
  a scheme for the Role, e.g. ``FirstnameL[astname]``.

- Teacher visits:

    https://chcko.eu/en/contents?School=noschool&Field=2020&Teacher=noteacher&Class=noclass&Role=-------

  The teacher is a student, too, but I suggest ``-------`` for the student field.
  This is the default for a logged in user.

  Alternatively:

  - open https://chcko.eu
  - Go to ``Org`` (top left)
  - Enter the IDs.
  - Press [OK].
  - Go to ``Contents``.

- Students visit a problem (here ``r.bu``) via:

    https://chcko.eu/en/contents?School=noschool&Field=2020&Teacher=noteacher&Class=noclass&Role=GabiB&r.bu
    https://chcko.eu/en/contents?School=noschool&Field=2020&Teacher=noteacher&Class=noclass&Role=LauraB&r.bu
    https://chcko.eu/en/contents?School=noschool&Field=2020&Teacher=noteacher&Class=noclass&Role=LiliB&r.bu
    ...

  Alternatively they can also do the steps through

  - ``Org`` on https://chcko.eu and
  - visit the problem afterwards via https://chcko.eu/en?r.bu.

- The teacher enters the URL ``.../en/done?<classId>&*&*``
  to see if everybody was successful.
  Note, that ``Class=`` is about setting current student,
  while ``classId`` refers to the data to be queried.
  From right to left this means:

  - any problem (``*``)
  - of any student (``*``)
  - of the class ``<classID>``. The actual class ID must be used.

  https://chcko.eu/en/done?noclass&*&*

  Students can query the results of all, too, and possibly help each other.

Reserve a Name
--------------

Login in.

Then

- Go to ``Org`` and choose a name.
- Alternatively, after having logged in, visit an URL with the names of you choice, e.g.:

  https://chcko.eu/en/org?School=noschool&Field=2020&Teacher=noteacher

Create a Class
--------------

In the ``Org`` tab,
the ``Role`` input box uses the first of ``;,`` as a separator
to create a whole class with no owner (independent of logged in or not).
Then send an email to the students,
with the link to be filled with their name:

  https://chcko.eu/en/todo?School=noschool&Field=2020&Teacher=noteacher&Class=noclass&Role=<name>

Or send each student separately the full link.

If the students log in, they take ownership of the role.

Assign
------

To assign to others, you need to be logged in.

In the ``contents`` tab choose the problems
or use an URL:

| https://chcko.eu/en/contents?r.a&r.ck or
| https://chcko.eu/en/contents?r.a&&r.ck

At the end of the page you can choose classes or students to assign to.
Assigning a course (with the ``&&``) assigns the problems individually.

URLs without problems cannot be assigned.

The students

- log in
- go to ``Todo``
- solve the assigned problems

Find problems
-------------

There is no full text search engine yet.
To find a problem, there are these alternatives:

- use the index page https://chcko.eu/en/contents
- clone author packages and use local text search (grep, ...)

Create Printout
---------------

If you add ``bare`` to the query string of the contents URL,
header and footer is dropped.
There is a printer symbol 🖶  at the bottom right, which does that.
Then you can

- save and open the file with a MS Word or Libre Office
- print from within your browser (possibly to a pdf file)
- use the command line with ``chrome`` or ``chromium`` to create a PDF

::

    chrome --enable-logging --headless --disable-gpu --print-to-pdf=/full/path/to.pdf http://chcko.eu/en/contents?r.bk&r.c&r.i&cheader=Homework&bare

Check Done
----------

To check the done problems of others, you need to be logged in.

Change to the teacher / class / Role.

- Go to the ``done`` tab.
- Add ``?*&*`` to the URL:

  https://chcko.eu/en/done?*&*

Clicking on the names for class, teacher, ... forwards to these URLs.

``*`` can be replaced by ``%2A``
when sending the link, because some programs drop the ``*``.

  https://chcko.eu/en/done?%2A&%2A

``*&*`` means: don't take the default but any ``student`` and ``problem``.
``?<school>&<period>&<teacher>&<class>&<student>&<problem>``
is *defaulted to the left* with the current role names *if omitted*.

See `done`_ for details on queries.

Remove an Assignment
--------------------

The ``todo`` page has the same query format as the ``done`` page.

  https://chcko.eu/en/todo?*&*

Shows the given (and not yet done) assignments and
allows to delete them selectively.

Assume Role
-----------

As a logged in user you can have more roles.
These roles are listed by clicking in the role field
on the ☰,
not on the link to the current role.
Click on an entry to assume another role.

Remove a Role
-------------

- Assume the role
- Go to the ``Org`` tab
- Choose ``delete``
- Confirm

There should be no easier way,
because you lose all the history of the role,
by deleting it.

Change a Role
-------------

Same as `Remove a Role`_,
but choose ``change`` instead.

This moves all the history associated with a role
to the new role and deletes the previous one.

``change`` is a way to

- leave a ``class`` (``teacher``, ``period``, ``school``)
- and join another one

without loosing one's history.

Content Packages
================

Example content layout::

    chcko-r
      ├── chcko
      │   ├── conf.py
      │   ├── _images
      │   │   ├── r_dg_c1.png
      │   │   ├── ...
      │   └── r
      │       ├── initdb.py
      │       ├── __init__.py
      │       ├── a
      │       │   ├── de.html
      │       │   ├── en.html
      │       │   └── __init__.py
      │       ├── b
      │       │   ├── _de.html
      │       │   ├── de.rst
      │       │   ├── _en.html
      │       │   ├── en.rst
      │       │   ├── __init__.py
      │       │   └── vector_dot_cross.tex
      │       └── ...
      ├── ...
      ├── README.rst
      └── setup.py

Image file names in ``_images`` are either random or
otherwise unique by encoding author ID, problem ID, content and possibly language.

``__init__.py`` is always there.
Altogether it is a `Python <https://docs.python.org>`__ package,
with ``chcko`` `namespace <https://packaging.python.org/guides/packaging-namespace-packages/>`__

For problems, ``given()`` in ``__init__.py`` provides random numbers
and ``calc()`` solves the problem.
The parameters from ``given()`` can be overridden via the URL parameters.
``cheader`` URL parameter is text placed at the beginning of a page with problems.

Generated files start with ``_`` (``_<language_id>.html``).
``<language_id>.rst`` can contain `tikz <https://github.com/pgf-tikz/pgf>`__ images
and are statically converted to ``_<language_id>.html`` with::

  doit -kd. html

.. _`example`:

It is better to just stick to HTML, though.
HTML files are actually `stpl <https://github.com/rpuntaie/stpl>`__ template snippets,
for example ``r/a/en.html``::

    %path = "maths/trigonometry/sss"
    %kind = 0 #problems (see languages.py)
    %level = 11 # school year starting from elementary
    The sides of a triangle are
    a={{ g.a }},
    b={{ g.b }},
    c={{ g.c }}.
    How big are the angles (in degrees).
    %champles=['e.g.'+e for e in ['23.3','100','56.7']]
    %chq()

``chq`` (defined in 
`chelper.html <https://github.com/chcko/chcko/blob/master/chcko/chcko/chelper.html>`__
) creates the input field or shows the result,
according the output of ``calc()`` (normally a list of numbers),
if no ``idx`` is specified.
``chq`` optionally uses (if defined):

- ``chames``: as input names (per idx a html/tex string, e.g. r"\(\alpha\)")
- ``champles``: input examples ( " )
- ``chadios``: texts for **radio buttons** (a tuple per idx).
  ``calc()`` returns index number.
- ``checkos``: texts for **check boxes** (a tuble per idx).
  ``calc()`` returns list of indices as string of capital letters e.g. `AC` (``chr(65+i)``).

``g`` is returned by ``given()`` in ``__init__.py``:

.. code:: python

    import random
    import math as m
    from chcko.chcko.hlp import Struct
    def angle_deg(i, g):
        d = dict(zip('abc', ([g.a, g.b, g.c]*2)[i:]))
        return eval('180*acos((a*a+b*b-c*c)/2/a/b)/pi', {**d,'acos':m.acos,'pi':m.pi})
    def given():
        random.seed()
        a, b = random.sample(range(1, 10), 2)
        c = random.randrange(max(a - b + 1, b - a + 1), a + b)
        return Struct(a=a, b=b, c=c)
    def calc(g):
        return [angle_deg(i, g) for i in range(3)]
    names = [r'\(\alpha=\)', r'\(\beta=\)', r'\(\gamma=\)']

Non-problem texts are OK, too, but should *context-free*,
as they are composed to a page via the URL query string::

    https://chcko.eu/en/contents?r.a&r.by

Replace the ``&`` with ``&&`` to make a *course*::

    https://chcko.eu/en/contents?r.a&&r.by

In the URL

- content items are ``<author_id>.<content_id>``
- corresponding to the folder ``chcko/<author_id>/<content_id>/``

``initdb.py`` fills the database with content items. It is generated using::

    doit -kd. initdb

To add a new content package on https://chcko.eu:

- name it ``chcko-<author_id>``
  `not existing yet on pypi <https://pypi.org/search/?q=chcko>`__ (.e.g. ``r`` is already taken)
- test it locally
- upload it to `pypi`_
- add it to `requirements_ndb.txt <https://github.com/chcko/chcko/blob/master/requirements_ndb.txt>`__
  with a pull request

https://chcko.eu will be updated timely.

You can also run a server locally with::

    runchcko

If
`chcko <https://pypi.org/project/chcko/>`__
is not installed::

    runchcko_with_sql.py

Not installed content packages must be parallel to the main ``chcko`` folder.

New Package
-----------

Create a new content package with::

    runchcko --init chcko-<id>

You run this command also to fill
a repo you started on github and cloned.

Add a new content item with::

    doit -kd. new

or::

    doit -kd. rst

Edit the problem text in ``en.html`` using a `text editor`_.
See the example `above <#example>`_.

Then from the root of the content package::

    doit initdb
    runchcko

Tools
-----

If your are familiar with Linux, use it, possibly on a virtual machine
like `virtualbox <https://www.virtualbox.org/wiki/Downloads>`_.
But all the needed tools are also available for Windows and Mac.

On your PC you will need

- `git <https://git-scm.com/download/win>`_
- `python >= 3.7 <https://python.org/download>`_

Then in a CLI and folder of your choice::

  git clone https://github.com/chcko/chcko
  cd chcko
  pip install -r requirements_dev.txt
  pip install chcko

installs the python packages for development.

`Sphinx`_ is only needed if you use `RST`_.
And `Latex`_ is only needed if you use Sphinx plugins
(`sphinxcontrib.tikz <https://bitbucket.org/philexander/tikz>`__,
`sphinxcontrib.texfigure <https://github.com/prometheusresearch/sphinxcontrib-texfigure>`__).

Development
===========

Purpose
-------

Chcko is yet another solution for computer aided instructions (CAI).
The internet has a huge potential in teaching and learning.

The main purpose:

- Automatically correct problems

- Infrastructure to organize teaching (school, period, teacher, class, student)

- allow teachers/coaches to quickly check the problems of students

- The use is of course not confined to schools.
  Teachers, professors, tutors, coaches, students, autodidacts, ...
  can add problems and check themselves or others.

- Share content via separate content packages like `chcko-r`_.

- The numbers in problems are randomly generated.
  This way a problem can be reused.
  Students sitting next to each others in class will have different numbers and
  therefore cannot copy the results.

`Chcko`_ can be used remotely as well as in class.

In class students can use the browser on their smartphones to answer problems.
Teachers can immediately see, who answered correctly or who has not yet answered.
This way the teacher is faster to find
those students who have not yet memorized something
or have not yet understood a concept or a relationship.

Students can do problems immediately after the teacher's explanation in class in the same lesson.
This way the students

- need to pay attention,
  because they will have to know immediately afterwards

- cannot copy from others, because the numbers are different,
  even with problems only due in the next lesson

- do not need to admit that they have not understood,
  because the teacher sees, if they are unable to do the problem.
  Some students are too shy to ask.
  And there are other reasons,
  why student's incomprehension can stay unnoticed for too long.

The teacher cannot look at all the done problems of a class at the same time,
but the software can.
To do it sequentially in class would hold up the students.
If the teacher takes the exercise books home,
there is an unwanted delay in feedback for the students.

More parallelism in class is very important
in order to make the time spent there worthwhile for the students.

The time spent by a teacher to correct exercise books is also
better invested in a good preparation:

- how to motivate the students

- how to present the topic as easy as possible

- which questions to ask to practice and verify that the students have understood

Plan
====

- Every content has a unique ID = ID_author.ID_content.
  This way no ID coordination is necessary once the author has an ID.

- Every ID is also a folder

  - ID_author

    - ID_content1
    - ID_content2
    - ...

- IDs shall be as short as possible. They are best numbered through using a-z

  - numbers would not make it a Python identifier
  - capital letters would collide with windows case insensitivity for file names

- Every content folder contains Python code and language files

  - A Python part (``__init__.py``) to randomly generate for problems.
    It is also needed for content without numbers: just keep it empty.

  - Language template files (``en.html``, ``de.html``, ``it.html``, ``fr.html``,...)
    that will produce html.
    ``en.html`` should always be there as starting points for translations.

  - A static off-line step is possible, to create content from other formats,
    currently from restructured text files (``.rst``) using Sphinx.
    This allows to use Sphinx contributions like tikz and texfigure (``tex``,
    ``tikz``, ``chemfig``, ...) to create graphics.

- Human language context paths to problems and keywords are language dependent and are
  therefore in the language files.

- More problems can be combined in one URL / http request (*contents* query)
  e.g. to make a larger assignment.

- Problem/Content pages can reference other content or inline it
  via the template engine (``% include(`r.cy`)`` for html or or *:inl:`r.cy`* for RST).

- Answers to problems are stored in a DB and combined with the
  language texts during loading.

- A user role is identified by an ID path/hierarchy::

    school 1-n period 1-n teacher 1-n class 1-n student

- Via this hierarchy a teacher has fast access to the done problems
  of his classes and students via an URL query.

- Teachers can assign problems to their classes/students, which they access via a *todo* query

- Teachers see what their classes/students have done so far (*done* query)

- Users initially get a generated role (generated random strings for each),
  which they can change, though (*org* query).
  There users can choose a color to help then see in which role they are.

- Registered users can have more roles.
  Registration can also be done via Google, Twitter, Facebook or LinkedIn.

Design
======

The code tries to stay minimal:
Python 3 with `bottle`_ and a DB for the roles and problems.

Database:

The data model is::

  school 1-n period 1-n teacher 1-n class 1-n student 1-n problem

The first 5 are called a role.
A user has more roles.

DB is there for answers to problems, not for the problem texts.

- On `GCP`_, the DB is DataStore using `ndb`_
- On other server the DB is a SQL database using `SqlAlchemy`_

Environment Variables
---------------------

:CHCKOSECRET: a secret used to encode the user token cookie
:CHCKOPORT: used to change port for local server
:SOCIAL_AUTH_<PROVIDER>_KEY: for social login
:SOCIAL_AUTH_<PROVIDER>_SECRET: for social login


.. :CHCKO_MAIL_CREDENTIAL: used for verifying email addresses
   (currently not used due to with_email_verification=False)

Queries
-------

The URL format is::

  URL = "https://"domain"/"lang"/"page"
  domain = "chcko.eu"
  lang = "en"|"de"|...
  page = ["contents"]["?"{author"."problem["="count]"&"}]
         | "done"[rlinc]
         | "todo"
         | "org"
  rlinc = [[[[[school&]period&]teacher&]class&]student&]("*"|query)
  query = {field("~"|"="|"!"|"<"|">")value","}

If ``<lang>`` is dropped, the last language or the browser setting is used.
See `languages.py`_.

``<page>`` is one of ``contents``, ``done``, ``todo``, ``org``.
``contents`` is default, if dropped.

``<query>`` starts after the ``?`` and it is a ``&``-separated list.
``<query>`` can contain
``School=<LLL>&Field=<DDD>&Teacher=<RRR>&Class=<SSS>&Role=<TTT>``
for all pages.

contents
^^^^^^^^

With ``../<lang>/contents`` all current contents are listed. One can select more entries here.

``../en/contents?r.a&r.by=2`` (``r.a`` is equivalent to ``r.a=1``) would create
an English content page with one ``r.a`` and two ``r.by`` problems.
``../en/?r.a&r.by=2`` is the same, i.e. ``contents`` is the default page.

Use ``&&`` instead of ``&`` to show one problem at a time (**course**).

For logged-in users it is possible
to make **assignments** to class/students with the same School-Field-Teacher prefix.
You must have created the teacher role, before the others.

Problems have more questions and every question has points associated (default 1).
After checking the entered values at the top there will be a summary of achieved
points/total points twice, once not counting fields left empty.

The ``contents`` index can be limited with:

- ``link``: the author id
- ``level``: corresponds to school year starting from elemntary (1, 2, ...)
- ``kind``: problems texts courses examples summaries formal fragments remarks
  citations definitions theorems corollaries lemmas propositions axioms
  conjectures claims identities paradoxes meta
- ``path``: as given in the header of the content sources

done
^^^^

``../<lang>/done`` lists the done problems with date and time and whether they were correct.
One can open every done problem or do it again.
It is possible to delete the selected problems.

The query

``../<lang>/done?<school>&<period>&<teacher>&<class>&<student>&<problem>``

allows

- a student to filter his problems
- a teacher to see the problems of his classes or students

Omitted entries *on the left* will be filled by the corresponding current role IDs.
Therefore a student only needs ``<problem>``, if it should be filtered at all.
``<..>`` are placeholders for the actual strings.

For 'no restriction' ``*`` is used.

An entry has this format::

    name|field op value[,field op value[,...]]

- ``name`` is the name of the record
- ``field`` is a field of the record

    All records have a name, ``userkey`` and ``created``. School, Field,
    Teacher and Class have no other fields.  In addition Role has ``color``
    and Problem has ``query_string``, ``lang``, ``given``, ``created``,
    ``answered``, ``collection``, ``inputids``, ``results``, ``oks``,
    ``points``, ``answers``, ``nr``.

- ``op`` consists of ``~=!<>``, where ``~`` means ``=``.
  For the age of a problem (since ``created``)
  these abbreviations can be used::

    d=days, H=hours, M=minutes, S=seconds

``1DK&*&d>3,d<1`` would show all problems younger than 3 days (``d``) and
older than one day of students from class ``1DK``

.. admonition:: suggestion

    Bookmark often used requests.

Registered user's data is protected against queries from anonymous users or other registered users.

todo
^^^^

``../<lang>/todo`` lists the assignments with date/time given and date/time due.

org
^^^

``../<lang>/org`` allows to add, change or delete IDs for
School, Field, Teacher, Class and Role.
For fields left empty 

- ``-`` is used for logged in users
- a random ID is generated non-logged-in users

Setting role IDs fails, if the role is owned already.
Role prefixes of others are italic.
These other users can query your done problems.

``new`` will create a new role.

``change`` will change the identification of the current role,
i.e. all the problems done will be copied over.

``delete`` will delete the role and all its done problems.

A **color** can be chosen to more easily see in which role one is.

Permissions
-----------

One level of privacy is via the IDs you choose.  How the IDs link to the
real things is only know to you.  You could use first or last letter of names,
add some additional characters, or do some other obfuscation, without
compromising an easy mapping to the real things or person for your purpose.

All unregistered users fall into one user category. Therefore every other
unregistered user can query all other unregistered users' problems (non-owned).

A logged-in user assumes ownership of non-owned roles.

If you register and create instances of school, period, teacher, class and student,
then they are associated to you as a user (owned).
Then you can query all instances below your instance in the hierarchy::

  School
      n Fields
          n Teachers
              n Classes
                  n Roles


E.g.

- If a teacher role belongs to you, then classes and students that use the same
  IDs up to and inclusive teacher as your IDs, then you will be able to query them in the
  ``done`` page, even if they belong to some other user.

- A director in an educational institution could make a School ID. If all teachers
  use the same School ID, then the director will be able to query the whole hierarchy.


On the other hand, if you start your query above an instance that does not belong
to you, you will not see anything below, even if you have instances somewhere
in the deeper levels of the hierarchy.

In ``.../<lang>/done?<school>&<period>&<teacher>&<class>&<student>&<problem>``
you can drop instances from the left, immediately after the ``?``.
``.../<lang>/done?aclass&*&d>2`` would query all problems of any student of class ``aclass``
not older than 2 days. For this to work ``aclass`` needs to belong to you.
If it does not, but the teacher role above belongs to your, then you can still query
by entering ``.../<lang>/done?ateacher&aclass&*&d>2``.

History
=======

2013
----

As I was about to engage in a teaching job in the beginning of 2013 I was
looking for a way adequate for our times

- to follow the progress of my students
- to automate certain activities

I did not find a finished solution fitting to my ideas,
but I found Google AppEngine, which seemed to be a good basis for an own project.

During my teaching job it was still in a very unsophisticated state,
but it was usable already. During that time I added mostly problems, some summaries
or other texts that did fit into the topics in class.

The first name, `mamchecker`_,
came about from this school's abbreviation of the subject mathematics as MAM.

Since summer 2013 I restructured the code and added user management
and I translated the problems and texts into English.

As I did not continue teaching in autumn,
my major motivation for the additional effort was to make my initial effort
usable for others.

2020
----

I was kept busy 5+ years by a employment.
Now I revisited the project,

- renamed it to `chcko`_
- updated it to Python 3 and
- to the change at Google AppEngine (now part of `GCP`):
  `ndb`_ changes, no email any more
- added support for SQL databases using `sqlalchemy`_
- made it a python package `chcko`_
- separated the content to a separate `chcko-r`_ package,
  as an example
- made some fixes

.. _`bottle`: https://bottlepy.org/docs/dev/
.. _`GCP`: https://en.wikipedia.org/wiki/Google_Cloud_Platform
.. _`ndb`: https://github.com/googleapis/python-ndb
.. _`SqlAlchemy`: https://github.com/sqlalchemy/sqlalchemy
.. _`chcko`: https://github.com/chcko/chcko
.. _`chcko-r`: https://github.com/chcko/chcko-r
.. _`mamchecker`: https://github.com/mamchecker/mamchecker
.. _`languages.py`: https://github.com/chcko/chcko/blob/master/chcko/chcko/languages.py
.. _`pypi`: https://pypi.org/
.. _`rst`: https://docutils.sourceforge.io/docs/user/rst/quickref.html
.. _`sphinx`: https://www.sphinx-doc.org/en/master/
.. _`latex`: https://www.latex-project.org/get/
.. _`text editor`: https://www.slant.co/topics/3418/~best-open-source-programming-text-editors


