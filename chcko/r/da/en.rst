.. raw:: html

    %path = "ideas"
    %kind = kinda["meta"]
    %level = 0
    <!-- html -->

.. role:: asis(raw)
    :format: html latex


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

    - A Python part (``__init__.py``) to randomly generate for exercises (not
      needed for content)

    - Language template files (``en.html``, ``de.html``, ``it.html``, ``fr.html``,...) 
      that will produce html.
      en.html should always be there as starting points for translations.

    - A static off-line step is possible to create content from other formats,
      currently from restructured text files (.rst) using Sphinx.
      This allows to use Sphinx contributions like tikz and texfigure (``tex``,
      ``tikz``, ``chemfig``, ...) to create graphics.

- Human language context paths to exercises and keywords are language dependent and are
  therefore in the language files.

- More exercises can be combined in one URL / http request (Content query)
  e.g. to make a larger assignment.

- Exercises/Content pages can reference other content or inline it
  via the template engine.

- Answers to exercises are stored in a db and combined with the 
  language texts during loading.

- A user context/role is identified by an ID path/hierarchy::

  school 1-n period 1-n teacher 1-n class 1-n student

- Via this hierarchy a teacher has fast access to the done exercises
  of his classes and students via an URL query.

- Teachers can assign exercises to their classes/students, which they access via a Todo query

- Teachers see what their classes/students have done so far (Done query)

- Users initially get a generated context/role (generated random strings for each),
  which they can change, though (Edits query).
  There users can choose a color to help then see in which context/role they are.

- Registered users can have more contexts/roles (Contexts query).
  Registration can also be done via Google, Twitter, Facebook or LinkedIn.

