================
Working with Git
================

Git resources and tutorials
===========================

* `Git basics crash-course <http://git-scm.com/book/ch1-3.html>`_ -- how Git
  works and how does it differ from other VCSs. Part of the free `Pro Git book
  <http://git-scm.com/book>`_

* `Setting up Git <http://help.github.com/set-up-git-redirect>`_ -- a tutorial
  from Github_ on how to get started with Git on all the major OSs.

* `Git Reference <http://gitref.org/>`_ `is meant to be a quick reference for
  learning and remembering the most important and commonly used Git commands.`
  Also by the Github_ team.

* An introductory talk about Git by Karel Minařík:
  `video <http://webexpo.stream.cz/515013-karel-minarik-verzovani-kodu-s-gitem>`_
  & `slides <http://www.slideshare.net/karmi/verzovani-kodu-s-gitem-karel-minarik>`_.


.. note:: Basically, if you don't know how to do something in Git, just search
  `Stack Overflow`_...


.. _Stack Overflow: http://stackoverflow.com/search?q=how+do+you+...+in+git
.. _Github: https://github.com/


If you're on Windows
====================
you could try TortoiseGit_.


.. _TortoiseGit: http://code.google.com/p/tortoisegit/


If you decide to use the command-line interface
===============================================
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
