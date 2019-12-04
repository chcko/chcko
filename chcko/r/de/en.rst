.. raw:: html

    %path = "query rights"
    %kind = kinda["meta"]
    %level = 0 
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


One level of privacy is via the IDs you choose.  How the IDs link to the
real things is only know to you.  You could use first or last letter of names,
add some additional characters, or do some other obfuscation, without
compromising an easy mapping to the real things or person for your purpose.

All unregistered users fall into one user category.  Therefore every other
unregistered user can query all other unregistered users' exercises.

If you register and create instances of school, period, teacher, class and student,
then they are associated to you as a user.
Then you can query all instances below your instance in the hierarchy

| School
|     n Periods
|         n Teachers
|             n Classes
|                 n Students
    

E.g.

- If a teacher role belongs to you, then classes and students that use the same
  IDs up to and inclusive teacher as your IDs, then you will be able to query them in the
  ``done`` page, even if they belong to some other user.

- A director in an educational institution could make a School ID. If all teachers
  use the same School ID, then the director will be able to query the whole hierarchy.


On the other hand, if you start your query above an instance that does not belong
to you, you will not see anything below, even if you have instances somewhere
in the deeper levels of the hierarchy.

In ``/<lang>/done?<school>&<period>&<teacher>&<class>&<student>&<problem>``
you can drop instances from the left, immediately after the ``?``.
``/<lang>/done?aclass&*&d>2`` would query all problems of any student of class ``aclass``
not older than 2 days. For this to work ``aclass`` needs to belong to you.
If it does not, but the teacher role above belongs to your, then you can still query
by entering ``/<lang>/done?ateacher&aclass&*&d>2``.

