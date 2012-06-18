Soho - a static web site generator
==================================

Soho is a static web site generator. Yet another one? Yes. And I am
afraid it may not be more extensible, faster or in any way better than
the multitude of other similar tools. I wrote a first version of it a
few years ago (when there were less choice and none fit my needs) and
wanted to continue using the same source files for a couple of my web
sites.

- Soho is small. It is only a few hundred lines long and can easily be
  read, evaluated and tweaked.

- Soho currently supports reStructuredText and `Page Templates`_
  (a.k.a. Zope Page Templates) and obviously HTML but it may be
  extended to support other markup languages (e.g. Markdown) as well
  as other templating systems (e.g. Jinja).

- Soho can generate web sites in multiple languages and supports
  :abbr:`i18n (internationalization)` through GNU gettext files. For
  further details, see the related section in the :ref:`tutorial`.

- Soho does **not** automatically generate a blog-like archive site
  structure, or anything usually needed by blogs (such as tags or
  syndication feeds). If you need a blog generator, you may want to
  look at other tools (`Pelican`_ seems to be a popular choice).

.. _Page Templates: http://pagetemplates.org/docs/latest/

.. _Pelican: http://pelican.notmyidea.org/


Topics
------

.. toctree::
   :maxdepth: 2

   basics.rst
   installation.rst
   tutorial.rst
   ref.rst
   dev.rst
   changes.rst
   api.rst