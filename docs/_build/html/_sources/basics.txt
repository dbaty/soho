======
Basics
======

Soho consists of a single command-line program called ``soho-build``.
Running it on a specially structured directory will generate HTML
files, copy assets (such as images, CSS or JavaScript files) and
generate a `site map <http://www.sitemaps.org/>`_.

For each file to process (thus excluding assets), the following tasks
are done:

1. Generate HTML from the source file. The source file may be written
   in a special markup such as reStructuredText or directly in
   HTML. In all cases, a generator is chosen based on the file
   extension and returns an HTML fragment.

2. Apply a template to this HTML fragment. Currently, only Page
   Templates (also known as Zope Page Templates or ZPT) is supported,
   but Soho can be extended to support other templating systems. When
   applying the template, additional bindings can be provided through
   a metadata file (or directly in the source file if possible,
   e.g. if the source file is in reStructuredText).

All in all, here is a diagram of the process:

.. image:: _static/process.png
   :width: 634
   :height: 68
   :align: center
   :alt: A representation of Soho's process