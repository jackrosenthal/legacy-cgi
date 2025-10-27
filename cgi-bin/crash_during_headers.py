#!/usr/bin/env python3
"""Test CGI script that crashes DURING header output.

This tests cgitb when some headers have been output but the
blank line separating headers from body hasn't been sent yet.
"""
import cgitb

cgitb.enable()

print("Content-Type: text/plain")
print("X-Custom-Header: some-value")

raise ValueError("crash during header output")
