.. _tutorial_4_i18n:

==============================================
Internationalization and metadata on directory
==============================================

Here, we will build a web site with a more complex structure and
content in two languages: English and French. We will start from
scratch with a new empty directory:

.. code-block:: bash

   $ mkdir site2
   $ cd site2
   $ export SITE_ROOT=`pwd`

Again, the ``SITE_ROOT`` environment variable is not used by Soho but
will be useful to keep track of directory changes below.

The web site will have two sections, one for each language:

.. code-block:: bash

   $ cd src
   $ mkdir en
   $ mkdir fr

Once we have that, we may proceed and add content with two source
files in each section. First, ``src/en/index.html``:

.. literalinclude:: _tutorial/4-i18n/src/en/index.html
   :language: html

Then ``src/en/contact.html``:

.. literalinclude:: _tutorial/4-i18n/src/en/contact.html
   :language: html

And an home page in French in ``fr/index.html``:

.. literalinclude:: _tutorial/4-i18n/src/fr/index.html
   :language: html

Finally, the contact page in ``src/fr/contact.html``:

.. literalinclude:: _tutorial/4-i18n/src/fr/contact.html
   :language: html

Until now, this is very similar to what we have done in the previous
section of the tutorial. We have translated everything in source
files. We will now add some automatically translated content in the
template (in ``templates/layout.pt``):

.. literalinclude:: _tutorial/4-i18n/templates/layout.pt
   :language: xml
   :linenos:
   :emphasize-lines: 5, 7, 8-10

This is the same template as in the previous section except for the
highlighted lines. As you can see, we set the :abbr:`i18n
(internationalization)` domain at line 7. We also define a link whose
text will be automatically translated at line 10.

The template uses a CSS file, so you may want to copy the CSS file of
the previous section to a new ``assets/css`` directory.

Now we must set the translation somewhere. The default text ("Contact
me") is in English, so we only need to define the translation in
French. This must be done in a file that follows the GNU gettext
format. We could write this file from scratch (the format is simple
enough), but we will use Python tools to help us instead:

- Babel, which provides tools that will help us generate the
  translation files;

- Lingua, which provides message extractors. In other words, Lingua
  detects which messages have to be translated.

.. warning::

   As of this writing, Babel and Lingua support of Python 3 is
   unknown. See the `note below <#note-about-babel-and-lingua>`_ for
   an alternative.

.. code-block:: bash

   $ easy_install Babel lingua

(As usual, you may use ``pip install`` instead of ``easy_install``.)

For Babel to work, we can use a dummy ``setup.py`` file in the root
directory of our web site (at the same level as ``src``). Such files
are usually written to describe and create Python packages. Here, we
will only use the portion that is needed by Babel.

.. literalinclude:: _tutorial/4-i18n/setup.py
   :language: python

These few lines instruct Babel to use Lingua to extract messages from
templates (``*.pt`` files in ``templates``) and metadata files
(``*.meta.py``). As you can see, this file is very simple and can be
reused for any Soho web site.

We also need to tell Babel where we want the translation files to be
stored. We can do so in a ``setup.cfg`` file.

.. literalinclude:: _tutorial/4-i18n/setup.cfg
   :language: ini

This file tells Babel about the i18n domain that we want to handle
(``tutorial``), the path where files will be created (a ``locale``
directory, which is the standard name and the default in Soho) and a
few other settings that you may read about in `Babel documentation
<http://babel.edgewall.org/wiki/Documentation/index.html>`_. We will
create this directory and get ready to generate our translation files:

.. code-block:: bash

   $ cd $SITE_ROOT
   $ mkdir locale
   $ ls
   assets    locale    setup.cfg    setup.py    sohoconf.py    src    templates    www

First, we extract messages from our template with the
``extract_messages`` command:

.. code-block:: bash

   $ python setup.py extract_messages
   running extract_messages
   extracting messages from templates/layout.pt
   writing PO template file to locale/tutorial.pot
   $ ls locale
   tutorial.pot

This ``tutorial.pot`` file is a template. It contains a preamble and a
list of messages to be translated:

.. code-block:: bash

   $ tail -n 4 locale/tutorial.pot 
   #: templates/layout.pt:10
   msgid "Contact me!"
   msgstr ""

As indicated above, our message is already in English, so we need only
a French translation that we will create with the ``init_catalog``
command:

.. code-block:: bash

   $ python setup.py init_catalog -l fr
   running init_catalog
   creating catalog 'locale/fr/LC_MESSAGES/tutorial.po' based on 'locale/tutorial.pot'

A "catalog" has been created in the indicated path and it will look
very much like the ``tutorial.pot`` template above. The preamble will
be slightly different, but the last lines should be the same:

.. code-block:: bash

   $ tail -n 4 locale/fr/LC_MESSAGES/tutorial.po
   #: templates/layout.pt:10
   msgid "Contact me!"
   msgstr ""

You may edit this new ``tutorial.po`` file and add a translation (see
the highlighted line below):

.. literalinclude:: _tutorial/4-i18n/locale/fr/LC_MESSAGES/tutorial.po
   :language: po
   :emphasize-lines: 22

Once the ``tutorial.po`` file is ready, you have to compile it (into a
``tutorial.mo`` file) with the ``compile_catalog`` command:

.. code-block:: bash

   $ python setup.py compile_catalog
   running compile_catalog
   1 of 1 messages (100%) translated in 'locale/fr/LC_MESSAGES/tutorial.po'
   compiling catalog 'locale/fr/LC_MESSAGES/tutorial.po' to 'locale/fr/LC_MESSAGES/tutorial.mo'

If you change your template and add new messages or change existing
messages, you will need to perform a similar set of commands:

.. code-block:: bash

   $ # change template and add or modify messages to translate
   $ python setup.py extract_messages
   $ python setup.py update_catalog
   $ # edit your updated '.po' file
   $ python setup.py compile_catalog

Note that you need to run the ``init_catalog`` command only once.
Afterwards, you will have to run the ``update_catalog`` command.

.. note::

   .. _note-about-babel-and-lingua:

   As indicated above, you do not have to use Babel and Lingua to
   generate the translation files. You may very well create the
   ``.po`` by hand and generate the compiled ``.mo`` file with
   ``msgfmt``. However, having tools (be it Babel and Lingua or
   others) extract messages from your templates and metadata files is
   very valuable and can save a lot of time.

This is all good, we have translated our message. But we still need to
indicate to Soho that the ``en`` section has content in English and
the ``fr`` section has content in French, otherwise the template will
not know which language to translate the "Contact me!" message to. The
language should be set in a metadata file, under the ``locale``
binding. Since all files of the ``en`` directory are indeed in
English, we can set the metadata on the directory itself (as a file
named ``en/.meta.py``) and it will be inherited by all its files:

.. literalinclude:: _tutorial/4-i18n/src/en/.meta.py
   :language: python

As well, we create a similar file in ``fr/.meta.py``:

.. literalinclude:: _tutorial/4-i18n/src/fr/.meta.py
   :language: python

The template still expects a ``title`` key in the metadata, so we need
to indicate this for each source file. For example, in
``en/index.html.meta.py``:

.. literalinclude:: _tutorial/4-i18n/src/en/index.html.meta.py
   :language: python

Let's check that we have all expected files:

.. code-block:: bash

   $ ls -R
   assets    locale    setup.cfg    setup.py    sohoconf.py    src    templates    www

   ./assets:
   css

   ./assets/css:
   style.css

   ./locale:
   fr    tutorial.pot

   ./locale/fr:
   LC_MESSAGES

   ./locale/fr/LC_MESSAGES:
   tutorial.mo    tutorial.po

   ./src:
   en    fr

   ./src/en:
   contact.html    contact.html.meta.py    index.html    index.html.meta.py

   ./src/fr:
   contact.html    contact.html.meta.py    index.html    index.html.meta.py

   ./templates:
   layout.pt

All right, we can generate our web site:

.. code-block:: bash

   $ soho-build
   <date> - INFO - Copying assets...
   <date> - INFO - Copying "/path/to/site2/assets/css/style.css" to "/path/to/site2/www/css/style.css"
   <date> - INFO - Building HTML files...
   <date> - INFO - Processing "/path/to/site2/src/en/contact.html" (writing in "/path/to/site2/www/en/contact.html").
   <date> - INFO - Processing "/path/to/site2/src/en/index.html" (writing in "/path/to/site2/www/en/index.html").
   <date> - INFO - Processing "/path/to/site2/src/fr/contact.html" (writing in "/path/to/site2/www/fr/contact.html").
   <date> - INFO - Processing "/path/to/site2/src/fr/index.html" (writing in "/path/to/site2/www/fr/index.html").
   <date> - INFO - Generating Sitemap...
   <date> - INFO - Done.

We can see that the "Contact me" message appears in the proper
language in each section of the site:

.. code-block:: bash

   $ head -n 12 www/en/index.html | tail -n 3
   <div class="footer">
    <a href="contact.html">Contact me!</a>
   </div>
   $ head -n 12 www/fr/index.html | tail -n 3
   <div class="footer">
     <a href="contact.html">Contactez-moi !</a>
   </div>

.. note::

   If you open the HTML pages in your browser (as in
   ``file:///path/to/site2/www/en/index.html``), you may find that the
   CSS is not loaded. This is because we indicated an absolute path
   (``/css/style.css``) instead of a relative path to cope with the
   multi-level structure of the site. You would need an HTTP server to
   have the CSS correctly loaded. Fortunately, Python comes with a
   very handy simple HTTP server that you can run with the following
   command::

       $ cd $SITE_ROOT
       $ cd www
       $ python -m SimpleHTTPServer 8000

   You can then see your site at http://localhost:8000/en/index.html.