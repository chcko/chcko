.. raw:: html

    %path = "queries"
    %kind = kinda["meta"]
    %level = 0
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

URL
...

The URL format is ``../<lang>/<page>?<request>``.

``<lang>`` is ``en``, ``de``, ...  (see ``languages.py``).
It will remember your last language or use the browser setting, if dropped.

``<page>`` is one of ``content``, ``done``, ``todo``, ``edits`` and ``contexts``.
``contexts`` requires a registered user, who can have more contexts/roles.
``content`` is default, if dropped.

``<request>`` starts after the ``?`` and it is a ``&``-separated list, which can contain 
``School=<LLL>&Period=<DDD>&Teacher=<RRR>&Class=<SSS>&Student=<TTT>``
for all pages.

content
.......

With ``../<lang>/content`` all current contents are listed. One can select more entries here.

``../en/content?r.a&r.by=2`` (``r.a`` is equivalent to ``r.a=1``) would create
an English content page with one ``r.a`` and two ``r.by`` exercises.
``../en/?r.a&r.by=2`` is the same, i.e. ``content`` is the default page.

For registered users this page allows to make **assignments** to class/students with the same
School-Period-Teacher prefix. You must have selected a context where the teacher role
belongs to you, though, i.e. you created that teacher ID.

Exercises have more questions and every question has points associated (default 1). 
After checking the entered values at the top there will be a summary of achieved
points/total points twice, once not counting fields left empty.

done
....

``../<lang>/done`` lists the done exercises with date and time and whether they were correct.
One can open every exercise or do it again. It is possible to delete the selected exercises.

The query

``../<lang>/done?<school>&<period>&<teacher>&<class>&<student>&<exercise>`` 

allows 

- a student to filter his exercises
- a teacher to see the exercises of his classes or students

From the left, dropped entries will be filled by the corresponding current context IDs.
Therefore a student only needs ``<exercise>``, if it should be filtered at all. 
``<..>`` are placeholders for the actual strings.

For 'no restriction' ``*`` can be used. 

An entry has this format::

    name|field op value[,field op value[,...]]

- ``name`` is the name of the record
- ``field`` is a field of the record

    All records have a name, ``userkey`` and ``created``. School, Period,
    Teacher and Class have no other fields.  In addition Student has ``color``
    and Problem has ``query_string``, ``lang``, ``given``, ``created``,
    ``answered``, ``collection``, ``inputids``, ``results``, ``oks``,
    ``points``, ``answers``, ``nr``.

- ``op`` consists of ``~=!<>``, where ``~`` means ``=``.
  For the age (``answered``) of the exercise these abbreviations can be used::

    d=days, H=hours, M=minutes, S=seconds

``1DK&*&d>3,d<1`` would show all exercises younger than 3 days (``d``) and
older than one day of students from class ``1DK`` 

.. admonition:: suggestion

    Bookmark often used requests.

Registered user's data is protected against queries from anonymous users or other registered users.

todo
....

``../<lang>/todo`` lists the assignments with date/time given and date/time due.

edits
.....

``../<lang>/edits`` allows to add, change or delete IDs for 
School, Period, Teacher, Class and Student.
For fields left empty the IDs ``myschool``, ``myperiod``, ``myteacher``,
``myclass`` and ``myself`` are used.

If the set of IDs for a full context path is used already, then it will be told.
If context path prefixes of others are used, it will be recognizable by their italic format.
These other users can query your done exercises.

``new`` will create a new context/role.

``change`` will change the identification of the current context/role, i.e. all the exercise done will be copied over.

``delete`` will delete the context/role and all its done exercises.

A **color** can be chosen to more easily see in which context/role one is.

contexts
........

``../<lang>/contexts`` lists all contexts/roles of the currently registered user.

These contexts/roles can also be accessed via a drop down menu when hovering over the student ID.
Then the currently open page will be reopened with the new context/role.


