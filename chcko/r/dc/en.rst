.. raw:: html

    %path = "participate"
    %kind = kinda["meta"]
    %level = 0
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

Skills
------

You need to know:

- some HTML
- some Python (with numpy and sympy)
- possibly Javascript 
- basic understanding and working with the tools

Tools
-----

If your are a little familiar with Linux, use it, possibly on a virtual machine
like `virtualbox <https://www.virtualbox.org/wiki/Downloads>`_ . 
Then you can use ``git`` and other tools with less problems 
(e.g. easy installation via package managers, symlinks supported,...).
But all the needed tools are also available for Windows and Mac.

Collaboration is done via `github <https://github.com/mamchecker>`_.
Exercises contain Python code (also in the HTML templates), therefore
handling them like code is appropriate. Reviews are necessary for safety
reasons. 

On your PC you will need

- `git <http://rogerdudler.github.io/git-guide/>`_ 
  (use `msys git <http://msysgit.github.io/>`_ on Windows).
  `Introduction <http://git-scm.com/book/en/Getting-Started-First-Time-Git-Setup>`_

- `python <http://www.python.org/download/releases/2.7/>`_  
  with `pip <http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows>`_
  (Python 3 is not yet supported by Google Appengine)

- `google appengine <https://developers.google.com/appengine/downloads>`_

- `doit <http://pydoit.org/>`_ (``pip install doit``)

- `pytest <http://pytest.org/latest/>`_ for testing  (``pip install pytest``)

and optionally

- `sphinx <http://sphinx-doc.org/latest/install.html>`_ if you want to use restructured text (rst)
  (``pip install sphinx``). 

- latex (use `miktex <http://miktex.org/>`_ on Windows) for sphinx plugins
  (`sphinxcontrib.tikz <https://bitbucket.org/philexander/tikz>`_,
  `sphinxcontrib.texfigure <https://bitbucket.org/prometheus/sphinxcontrib-texfigure>`_).

- `coverage <http://nedbatchelder.com/code/coverage/>`_ (``pip install coverage``)

As browser Chrome has the best `HTML5 <http://html5test.com/results/desktop.html>`_ support
and a good debugging environment for Javascript.

For editing use your editor of choice. It should allow you to execute selected python code 
(`pydev <http://pydev.org/manual_adv_interactive_console.html>`_, `vim <http://www.vim.org/>`_).

Get Started
-----------

Fork it on github.

    - Use your browser to create a fork of Mamchecker on github

    - On your local command prompt you ``git clone`` your forked repository to a local folder
      (msys bash on Windows)::

        git clone --recursive https://github.com/mamchecker/mamchecker.git

      If you didn't use `--recursive <http://stackoverflow.com/questions/3796927/how-to-git-clone-including-submodules>`_ 
      you have to additionally do `git submodule update --init --recursive <http://stackoverflow.com/questions/9493645/fork-github-repo-with-submodules>`_).

Add yourself as author.

    - Register yourself with an ``author_id`` in the sources in ``authors.yaml``.
      ``default_lang: en`` influences the ``doit`` commands below.

    - Create a folder (parallel to the existing ``r`` folder) named with your author id.

Add exercises. To see how easy that is, look at the examples in the existing ``r`` folder.

    - Add a folder in your authors folder and populate it with ``__init__.py``, ``en.html``, ...
      then edit. To do this use ``doit``; it generates the next id and uses it to create a folder 
      (see ``nextids.yaml`` and ``dodo.py``):

      - ``doit -kd. new`` will add a folder, then you would manually add the files
      - ``doit -kd. problem`` adds a folder and ``__init__.py`` and ``<default_lang>.html``,
        add ``en.html`` and possibly others manually. Remove ``__init__.py``, if there is no code involved.
      - ``doit -kd. rst`` adds a folder and ``<default_lang>.rst``. 
        After editing ``doit -kd. html`` will convert rst files to html.
        Generated files start with a underscore. Sphinx generates e.g. ``_en.html`` from ``en.rst``.

    - ``__init__.py`` must provide the functions ``given`` and ``calc`` and
      optionally ``norm``, ``equal``, ``points`` and ``names``
      (see ``from_py`` in ``hlp.py`` and examples in the ``r``-folder).

    - ``<lang>.html`` is html and ``{{'{{}}'}}``-enclosed or ``%``-started python 
      (`SimpleTemplate <http://bottlepy.org/docs/dev/stpl.html>`_) just for the one exercise.
      Also use the template ``getorshow`` as done in the examples in the ``r``-folder.
      The generated HTML will be enclosed in a ``<div>`` 
      (see ``inc`` in ``util.py``).

    - ``<lang>.rst`` can use the roles ``inl`` for inlining and ``lnk`` to reference 
      (see ``inl.py`` and look for examples in the ``r``-folder).

    - At the beginning of the language file have the following lines, where

      - ``<kind>`` is one the language specific kind strings in ``kind.py``
      - ``level`` must be last and means years starting from elementary school (1, 2, ...)

      for ``<lang>.rst``::
        |
        | .. raw:: html
        |
        |     \%path = "path/to/create/a/hierarchical/order"
        |     \%kind = kinda["<kind>"]
        |     \%level = 0
        |     <!-- html -->
        |
        | .. role:: asis(raw)
        |     :format: html latex
        |

      for ``<lang>.html``::
        |
        |    \%path = "path/to/create/a/hierarchical/order"
        |    \%kind = kinda["<kind>"]
        |    \%level = 9
        |

    - From above the mamchecker folder (where app.yaml is) do ``dev_appserver mamchecker``
      and test your exercise on the browser (``http://localhost:8080/en/?<yourid>.<problemid>``).
      Check different nonsense,  almost correct and correct inputs.

Ready for commit.

    - ``doit -kd. initdb`` must be executed to generate ``initdb.py``, which
      creates the content overview page. If you have ``rst`` files, do ``doit -kd. html`` first.

    - On your local command prompt in the mamchecker folder do
      
        - ``git status``
        - ``git diff``
        - ``git commit -am "what you did"`` 
        - ``git push`` to your github repository 

   -  There is a test script which you can start locally. In your command prompt where ``dodo.py`` is
      do: 
      
        - ``doit test``. 
          
      This tests more than is needed, if you only added an exercise. 
      But do it, if you have made other changes in code.

Add your contribution to the main repository.

    - In the browser you create a **pull request**.
      This way all contributions come together.

