#!/usr/bin/env python3
"""Test CGI script that crashes AFTER HTML output has begun.

This tests cgitb when headers and some body content have already
been sent to the browser.
"""
import cgitb

cgitb.enable()

print("Content-Type: text/html")
print()
print("<html><head><title>Test Page</title></head>")
print("<body>")
print("<h1>Welcome to my page</h1>")
print("<p>Some content here...</p>")

raise ValueError("crash after HTML output")
