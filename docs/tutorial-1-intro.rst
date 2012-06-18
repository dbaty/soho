.. _tutorial_1_intro:

==================================================
Setting up the structure and creating source files
==================================================

Let's create a new directory that will contain our site: the source
files, assets (images, Javascript, CSS, etc.) and a Soho configuration
file.

.. code-block:: bash

   $ mkdir site1
   $ cd site1
   $ export SITE_ROOT=`pwd`

The last command is just a way to get an "anchor" to the root of your
site structure. It is not used by Soho at all but may prove useful in
the rest of this tutorial.

We need a directory for the source files. By default, Soho looks for a
directory named ``src`` so that is what we will use here.

.. code-block:: bash

  $ mkdir src
  $ cd src

We can already create our first source file there named ``index.rst``,
with the following content:

.. literalinclude:: _tutorial/1-intro/src/index.rst
   :language: rst

As you can see, there is a link to another file here, called
``second.html``, which we can create with the following content:

.. literalinclude:: _tutorial/1-intro/src/second.html
   :language: html

Now that we have our content, we need a template. By default,
templates are looked up in a ``templates`` directory next to the
``src`` directory (that we already have).

.. code-block:: bash

   $ cd $SITE_ROOT
   $ mkdir templates
   $ ls
   src    templates
   $ cd templates

We are going to create our first template named ``layout.pt`` in this
new ``templates`` directory. We will start with a very simple template
indeed:

.. literalinclude:: _tutorial/1-intro/templates/layout.pt
   :language: xml

We are using `Page Templates <http://pagetemplates.org/docs/latest>`_
(also known as Zope Page Templates or ZPT). As you can notice, the
only binding here is named ``body`` and contain the HTML fragment that
has been generated from our source files. We will see later that we
can pass additional bindings.

This is enough for a first test. We just need to add a configuration
file next to the ``src`` and ``templates`` directory, which we will
name ``sohoconf.py``. The configuration file is a regular Python file:

.. literalinclude:: _tutorial/1-intro/sohoconf.py
   :language: python

Here we need to disable some default values that correspond to
features that will be covered later. Let's check our files before
running Soho for the first time:

.. code-block:: bash

   $ cd $SITE_ROOT
   $ ls
   src  sohoconf.py     templates

We are ready to run:

.. code-block:: bash

   $ soho-build
   <date> - INFO - Building HTML files...
   <date> - INFO - Processing "/path/to/site1/src/index.rst" (writing in "/path/to/site1/www/index.html").
   <date> - INFO - Processing "/path/to/site1/src/second.html" (writing in "/path/to/site1/www/second.html").
   <date> - INFO - Generating Sitemap...
   <date> - INFO - Done.
   $ ls www
   index.html   second.html     sitemap.xml

As you can see, our source files have been transformed to HTML, the
template has been applied, and the resulting web site has been saved
in files in a new ``www`` directory. Also, Soho generated a Sitemap.

.. note::

   If you look closely at the generated ``sitemap.xml``, you may see
   that the URLs all have some kind of default prefix
   (``http://exemple.com/soho/default-base-url``). You may change this
   prefix by setting the ``base_url`` variable in the configuration
   file (if you do so, be sure to run ``soho-build`` with the
   ``--force`` command-line option).

You may continue with the tutorial by following the
:ref:`tutorial_2_assets` section.