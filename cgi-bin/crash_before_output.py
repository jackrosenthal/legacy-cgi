#!/usr/bin/env python3
"""Test CGI script that crashes BEFORE any output.

This tests cgitb's ability to output proper headers and HTML
when no output has been sent yet.
"""
import cgitb

cgitb.enable()

raise ValueError("crash before header output")
