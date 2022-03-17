Python CGI
==========

This is a fork of the standard library modules ``cgi`` and ``cgitb``.
They are slated to be removed from the Python standard libary in
Python 3.13 by PEP-594_.

.. _PEP-594: https://peps.python.org/pep-0594/

Installation
------------

Install the ``legacy-cgi`` package from PyPI::

  $ pip install legacy-cgi

Purpose
-------

The purpose of this fork is to support existing CGI scripts using
these modules.  Thus, compatibility is the primary goal.

Contributions are accepted, but should be focused on bug fixes instead
of new features or major refactoring.

New applications should look at the WSGI_ ecosystem.  There's a number
of highly-polished web frameworks available, and it's significantly
faster in a typical deployment given a new Python process does not
need created for each request.

.. _WSGI: https://wsgi.readthedocs.io
