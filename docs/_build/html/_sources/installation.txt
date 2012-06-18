============
Installation
============

You must have Python 2.7 or Python 3.2 installed. Other versions may
work but are not supported. As usual, it is recommended that you
install Soho within a `virtual environment
<http://www.virtualenv.org/en/latest/index.html>`_ (virtualenv).

Soho and required dependencies can be installed like this (of course,
you may use ``pip`` instead of ``easy_install``):

.. code-block:: bash

   $ easy_install Soho

Required dependencies are kept to a minimum. In fact, as of this
writing, there are no required dependency at all. Depending on the
features that you would like to use, you need to install the
corresponding extra requirements.

To use Page Templates:

.. code-block:: bash

   $ easy_install Soho[zpt]

To use the reStructuredText generator:

.. code-block:: bash

   $ easy_install Soho[rst]

If you are used to write documentation with Sphinx and the
reStructuredText directives it defines (e.g. ``code-block``), you may
want to install Sphinx as well.

To benefit from :abbr:`i18n (internationalization)` support:

.. code-block:: bash

   $ easy_install Soho[i18n]

If you are feeling adventurous, you may install all optional
dependencies with the following command:

.. code-block:: bash

   $ easy_install Soho[all]

To check that Soho has been correctly installed, you may look for a
new ``soho-build`` executable file that should have been added to your
``PATH``:

.. code-block:: bash

   $ soho-build --version
   soho-build 0.8.0