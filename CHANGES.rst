List of releases of Soho
========================

unreleased
----------

- Fix bug in tests that caused functional tests to fail. This was due
  to the fact that "git clone" does not preserve file modification
  time: this caused test failures because we were diff'ing
  "sitemap.xml" files that do contain last modification time.


Soho 0.8.0 (2012-08-17)
-----------------------

Major rewrite. Old Soho projects should be easily moved to the new
format (see documentation).


Soho 0.7 (2008-02-17)
---------------------

First public release. Note that it was registered in PyPI as "soho"
(with a lowercase "s").
