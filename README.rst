Python CGI
==========

This is a fork of the standard library modules ``cgi`` and ``cgitb``.  They have
been removed from the Python standard libary in Python 3.13 by PEP-594_.

.. _PEP-594: https://peps.python.org/pep-0594/

Installation
------------

Depend upon ``legacy-cgi`` in your project.  It is recommended to use the marker
``python_version >= 3.13``, as while the package can install for older Python
versions, it won't have effect with a standard Python installation as the
built-in modules will take precedence.

For example, in a ``requirements.txt`` file::

  legacy-cgi; python_version >= 3.13

Or in a PEP-621 ``pyproject.toml`` file::

  [project]
  ...
  dependencies = [
      ...,
      "legacy-cgi; python_version >= '3.13'",
  ]

Purpose
-------

The purpose of this fork is to support existing CGI scripts using
these modules.  Thus, compatibility is the primary goal.

Contributions are accepted, but should be focused on bug fixes instead
of new features or major refactoring.

New applications should look at the ASGI_ or WSGI_ ecosystems.  There's a number
of highly-polished web frameworks available, and it's significantly faster in a
typical deployment given a new Python process does not need created for each
request.

.. _ASGI: https://asgi.readthedocs.io
.. _WSGI: https://wsgi.readthedocs.io

Documentation
-------------

See the official documentation for Python 3.12 and earlier for usage:

* `cgi module`_
* `cgitb module`_

.. _cgi module: https://docs.python.org/3.12/library/cgi.html
.. _cgitb module: https://docs.python.org/3.12/library/cgitb.html

The modules are not renamed, so code written for Python 3.12 or earlier should
work without modification with this package installed.
