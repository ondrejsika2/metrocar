================
Working with Git
================

.. todo:: TODO: find a decent crash-course Git tutorial (github?)


.. note:: Basically, if you don't know how to do something in Git, just search
  `Stack Overflow`_...

.. _Stack Overflow: http://stackoverflow.com/search?q=how+do+you+...+in+git


If you're on Windows
--------------------
you could try TortoiseGit_.


.. _TortoiseGit: http://code.google.com/p/tortoisegit/


If you decide to use the command-line interface like a real man
---------------------------------------------------------------
you might want to define some shortcuts for commonly used commands.

.. highlight:: bash

Here's a little inspiration::

    # shorter, less cluttered status
    alias gits='git status -s'

    # colored diff
    alias gitd='git diff --color'

    # diff of staged changes
    alias gitdc='git diff --color --cached'

    # colored log with commit messages and changed filenames
    alias gitl='git log --name-status --color'

    # log with full diffs
    alias gitld='git log -p --color'
