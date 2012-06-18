.. _tutorial_2_assets:

=============
Adding assets
=============

(This is a continuation of the first section of the tutorial entitled
:ref:`tutorial_1_intro`.)

Our web site is fine, although not visually appealing. As specialists
put it, it is ugly. We are going to use a CSS file to "enhance the
user experience" (i.e. make it look a bit better). We could put this
CSS file in the ``src`` directory, but it is not content per se. So we
will put it in a special directory named ``assets`` or, rather, in a
sub-directory called ``assets/css``.

.. code-block:: bash

   $ cd $SITE_ROOT
   $ mkdir -p assets/css
   $ ls
   assets    sohoconf.py    src    templates
   $ cd assets/css

Here is a very simple CSS file (which you may obviously improve):

.. literalinclude:: _tutorial/2-assets/assets/css/style.css
   :language: css

We need to indicate to Soho that we have a special directory for
assets. This is done in the ``sohoconf.py`` file with the
``asset_dir`` variable. You may remember that we set it to ``None`` in
the first section of the tutorial to indicate that we did not have any
asset directory. Here, we have different solutions to indicate the
directory. This is the same mechanism for all path settings in
Soho. We may indicate an absolute path like this:

.. code-block:: python

   asset_dir = '/path/to/your/site1/assets'

A usually better solution is to indicate a path relative to the
configuration file, like this (not the leading ``./``):

.. code-block:: python

   asset_dir = './assets'

In fact, this is the default value for ``asset_dir``, so you do not
have to provide it. Hence, the complete configuration file could look
like this:

.. literalinclude:: _tutorial/2-assets/sohoconf.py
   :language: python

We also need to add a link to this stylesheet in the template
(``templates/layout.pt``). Because we are good citizens, we will write
a valid HTML document:

.. literalinclude:: _tutorial/2-assets/templates/layout.pt
   :language: xml

We are ready to run Soho again:

.. code-block:: bash

   $ cd $SITE_ROOT
   $ ls
   assets    sohoconf.py    src    templates
   $ soho-build
   <date> - INFO - Copying assets...
   <date> - INFO - Copying "/path/to/site1/assets/css/style.css" to "/path/to/site1/www/css/style.css"
   <date> - INFO - Building HTML files...
   <date> - INFO - Done.

As you can see, only assets have been processed. This is because we
did not change any source file. However, we did change the template,
so we should force the processing of source files. This can be done
with the ``-f`` (or ``--force``) command-line option, like this:

.. code-block:: bash

   $ soho-build -f
   <date> - INFO - Copying assets...
   <date> - INFO - Copying "/path/to/site1/assets/css/style.css" to "/path/to/site1/www/css/style.css"
   <date> - INFO - Building HTML files...
   <date> - INFO - Processing "/path/to/site1/src/index.rst" (writing in "/path/to/site1/www/index.html").
   <date> - INFO - Processing "/path/to/site1/src/second.html" (writing in "/path/to/site1/www/second.html").
   <date> - INFO - Generating Sitemap...
   <date> - INFO - Done.

You may continue with the tutorial by following the
:ref:`tutorial_3_metadata` section.