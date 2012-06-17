.. _tutorial_3_metadata:

==============================
Metadata and template bindings
==============================

(This is a continuation of the second section of the tutorial entitled
:ref:`tutorial_2_assets`.)

You may have seen that since the last iteration of the template, we
now have a ``<title>`` tag. It would be a good thing to have it filled
with the title of each document. For this, additional bindings should
be passed to the template. This can be done by providing metadata
about each file (and even directories).

We will start by setting metadata on ``second.html``. Metadata are
looked up in ``*.meta.py`` files. Hence, we are going to create a
``second.html.meta.py`` file next to ``second.html``, with the
following content:

.. literalinclude:: _tutorial/3-metadata/src/second.html.meta.py
   :language: python

Metadata files are Python files so you may import modules, compute
things, etc. All symbols that are local to the file will be available
in a binding called ``md`` in the template.

We could hence change the template like this (changes appear on the
highlighted line):

.. literalinclude:: _tutorial/3-metadata/templates/layout.pt
   :language: xml
   :emphasize-lines: 4

We did set metadata for the ``second.html`` file but not for
``index.rst``. We could create an ``index.rst.meta.py`` like we did
above, but reStructuredText files can embed metadata. We will indicate
the title in the file itself, like this (see highlighted lines):

.. literalinclude:: _tutorial/3-metadata/src/index.rst
   :language: rst
   :emphasize-lines: 1,2

We are ready to run Soho again:

.. code-block:: bash

   $ cd $SITE_ROOT
   $ ls src
   index.rst    second.html    second.html.meta.py
   $ soho-build -f
   [...]

You should now see the title of each page in your web browser.

In fact, metadata can be set on directories in files named
``.meta.py``. The metadata of each file automatically inherits from
the metadata of the directory it lives in, as well as the directory
above (if any), and so on and so forth. We will see a use-case for
this in the next section entitled :ref:`tutorial_4_i18n`.
