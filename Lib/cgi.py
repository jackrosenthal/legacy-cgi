#!/usr/local/bin/python

"""Support module for CGI (Common Gateway Interface) scripts.

This module defines a number of utilities for use by CGI scripts written in 
Python.


Introduction
------------

A CGI script is invoked by an HTTP server, usually to process user
input submitted through an HTML <FORM> or <ISINPUT> element.

Most often, CGI scripts live in the server's special cgi-bin
directory.  The HTTP server places all sorts of information about the
request (such as the client's hostname, the requested URL, the query
string, and lots of other goodies) in the script's shell environment,
executes the script, and sends the script's output back to the client.

The script's input is connected to the client too, and sometimes the
form data is read this way; at other times the form data is passed via
the "query string" part of the URL.  This module (cgi.py) is intended
to take care of the different cases and provide a simpler interface to
the Python script.  It also provides a number of utilities that help
in debugging scripts, and the latest addition is support for file
uploads from a form (if your browser supports it -- Grail 0.3 and
Netscape 2.0 do).

The output of a CGI script should consist of two sections, separated
by a blank line.  The first section contains a number of headers,
telling the client what kind of data is following.  Python code to
generate a minimal header section looks like this:

	print "Content-type: text/html"	# HTML is following
	print				# blank line, end of headers

The second section is usually HTML, which allows the client software
to display nicely formatted text with header, in-line images, etc.
Here's Python code that prints a simple piece of HTML:

	print "<TITLE>CGI script output</TITLE>"
	print "<H1>This is my first CGI script</H1>"
	print "Hello, world!"

(It may not be fully legal HTML according to the letter of the
standard, but any browser will understand it.)


Using the cgi module
--------------------

Begin by writing "import cgi".  Don't use "from cgi import *" -- the
module defines all sorts of names for its own use that you don't want
in your namespace.

If you have a standard form, it's best to use the SvFormContentDict
class.  Instantiate the SvFormContentDict class exactly once: it
consumes any input on standard input, which can't be wound back (it's
a network connection, not a disk file).

The SvFormContentDict instance can be accessed as if it were a Python
dictionary.  For instance, the following code checks that the fields
"name" and "addr" are both set to a non-empty string:

	form = SvFormContentDict()
	form_ok = 0
	if form.has_key("name") and form.has_key("addr"):
		if form["name"] != "" and form["addr"] != "":
			form_ok = 1
	if not form_ok:
		print "<H1>Error</H1>"
		print "Please fill in the name and addr fields."
		return
	...actual form processing here...

If you have an input item of type "file" in your form and the client
supports file uploads, the value for that field, if present in the
form, is not a string but a tuple of (filename, content-type, data).


Overview of classes
-------------------

SvFormContentDict: single value form content as dictionary; described
above.

FormContentDict: multiple value form content as dictionary (the form
items are lists of values).  Useful if your form contains multiple
fields with the same name.

Other classes (FormContent, InterpFormContentDict) are present for
backwards compatibility only.


Overview of functions
---------------------

These are useful if you want more control, or if you want to employ
some of the algorithms implemented in this module in other
circumstances.

parse(): parse a form into a Python dictionary.

parse_qs(qs): parse a query string.

parse_multipart(...): parse input of type multipart/form-data (for
file uploads).

parse_header(string): parse a header like Content-type into a main
value and a dictionary of parameters.

test(): complete test program.

print_environ(): format the shell environment in HTML.

print_form(form): format a form in HTML.

print_environ_usage(): print a list of useful environment variables in
HTML.

escape(): convert the characters "&", "<" and ">" to HTML-safe
sequences.  Use this if you need to display text that might contain
such characters in HTML.  To translate URLs for inclusion in the HREF
attribute of an <A> tag, use urllib.quote().


Caring about security
---------------------

There's one important rule: if you invoke an external program (e.g.
via the os.system() or os.popen() functions), make very sure you don't
pass arbitrary strings received from the client to the shell.  This is
a well-known security hole whereby clever hackers anywhere on the web
can exploit a gullible CGI script to invoke arbitrary shell commands.
Even parts of the URL or field names cannot be trusted, since the
request doesn't have to come from your form!

To be on the safe side, if you must pass a string gotten from a form
to a shell command, you should make sure the string contains only
alphanumeric characters, dashes, underscores, and periods.


Installing your CGI script on a Unix system
-------------------------------------------

Read the documentation for your HTTP server and check with your local
system administrator to find the directory where CGI scripts should be
installed; usually this is in a directory cgi-bin in the server tree.

Make sure that your script is readable and executable by "others"; the
Unix file mode should be 755 (use "chmod 755 filename").  Make sure
that the first line of the script contains "#!" starting in column 1
followed by the pathname of the Python interpreter, for instance:

	#!/usr/local/bin/python

Make sure the Python interpreter exists and is executable by "others".

Make sure that any files your script needs to read or write are
readable or writable, respectively, by "others" -- their mode should
be 644 for readable and 666 for writable.  This is because, for
security reasons, the HTTP server executes your script as user
"nobody", without any special privileges.  It can only read (write,
execute) files that everybody can read (write, execute).  The current
directory at execution time is also different (it is usually the
server's cgi-bin directory) and the set of environment variables is
also different from what you get at login.  in particular, don't count
on the shell's search path for executables ($PATH) or the Python
module search path ($PYTHONPATH) to be set to anything interesting.

If you need to load modules from a directory which is not on Python's
default module search path, you can change the path in your script,
before importing other modules, e.g.:

	import sys
	sys.path.insert(0, "/usr/home/joe/lib/python")
	sys.path.insert(0, "/usr/local/lib/python")

(This way, the directory inserted last will be searched first!)

Instructions for non-Unix systems will vary; check your HTTP server's
documentation (it will usually have a section on CGI scripts).


Testing your CGI script
-----------------------

Unfortunately, a CGI script will generally not run when you try it
from the command line, and a script that works perfectly from the
command line may fail mysteriously when run from the server.  There's
one reason why you should still test your script from the command
line: if it contains a syntax error, the python interpreter won't
execute it at all, and the HTTP server will most likely send a cryptic
error to the client.

Assuming your script has no syntax errors, yet it does not work, you
have no choice but to read the next section:


Debugging CGI scripts
---------------------

First of all, check for trivial installation errors -- reading the
section above on installing your CGI script carefully can save you a
lot of time.  If you wonder whether you have understood the
installation procedure correctly, try installing a copy of this module
file (cgi.py) as a CGI script.  When invoked as a script, the file
will dump its environment and the contents of the form in HTML form.
Give it the right mode etc, and send it a request.  If it's installed
in the standard cgi-bin directory, it should be possible to send it a
request by entering a URL into your browser of the form:

	http://yourhostname/cgi-bin/cgi.py?name=Joe+Blow&addr=At+Home

If this gives an error of type 404, the server cannot find the script
-- perhaps you need to install it in a different directory.  If it
gives another error (e.g.  500), there's an installation problem that
you should fix before trying to go any further.  If you get a nicely
formatted listing of the environment and form content (in this
example, the fields should be listed as "addr" with value "At Home"
and "name" with value "Joe Blow"), the cgi.py script has been
installed correctly.  If you follow the same procedure for your own
script, you should now be able to debug it.

The next step could be to call the cgi module's test() function from
your script: replace its main code with the single statement

	cgi.test()
	
This should produce the same results as those gotten from installing
the cgi.py file itself.

When an ordinary Python script raises an unhandled exception
(e.g. because of a typo in a module name, a file that can't be opened,
etc.), the Python interpreter prints a nice traceback and exits.
While the Python interpreter will still do this when your CGI script
raises an exception, most likely the traceback will end up in one of
the HTTP server's log file, or be discarded altogether.

Fortunately, once you have managed to get your script to execute
*some* code, it is easy to catch exceptions and cause a traceback to
be printed.  The test() function below in this module is an example.
Here are the rules:

	1. Import the traceback module (before entering the
	   try-except!)
	
	2. Make sure you finish printing the headers and the blank
	   line early
	
	3. Assign sys.stderr to sys.stdout
	
	3. Wrap all remaining code in a try-except statement
	
	4. In the except clause, call traceback.print_exc()

For example:

	import sys
	import traceback
	print "Content-type: text/html"
	print
	sys.stderr = sys.stdout
	try:
		...your code here...
	except:
		print "\n\n<PRE>"
		traceback.print_exc()

Notes: The assignment to sys.stderr is needed because the traceback
prints to sys.stderr.  The print "\n\n<PRE>" statement is necessary to
disable the word wrapping in HTML.

If you suspect that there may be a problem in importing the traceback
module, you can use an even more robust approach (which only uses
built-in modules):

	import sys
	sys.stderr = sys.stdout
	print "Content-type: text/plain"
	print
	...your code here...

This relies on the Python interpreter to print the traceback.  The
content type of the output is set to plain text, which disables all
HTML processing.  If your script works, the raw HTML will be displayed
by your client.  If it raises an exception, most likely after the
first two lines have been printed, a traceback will be displayed.
Because no HTML interpretation is going on, the traceback will
readable.

Good luck!


Common problems and solutions
-----------------------------

- Most HTTP servers buffer the output from CGI scripts until the
script is completed.  This means that it is not possible to display a
progress report on the client's display while the script is running.

- Check the installation instructions above.

- Check the HTTP server's log files.  ("tail -f logfile" in a separate
window may be useful!)

- Always check a script for syntax errors first, by doing something
like "python script.py".

- When using any of the debugging techniques, don't forget to add
"import sys" to the top of the script.

- When invoking external programs, make sure they can be found.
Usually, this means using absolute path names -- $PATH is usually not
set to a very useful value in a CGI script.

- When reading or writing external files, make sure they can be read
or written by every user on the system.

- Don't try to give a CGI script a set-uid mode.  This doesn't work on
most systems, and is a security liability as well.


History
-------

Michael McLay started this module.  Steve Majewski changed the
interface to SvFormContentDict and FormContentDict.  The multipart
parsing was inspired by code submitted by Andreas Paepcke.  Guido van
Rossum rewrote, reformatted and documented the module and is currently
responsible for its maintenance.

"""


# Imports
# =======

import string
import regsub
import sys
import os
import urllib


# A shorthand for os.environ
environ = os.environ


# Parsing functions
# =================

def parse(fp=None):
	"""Parse a query in the environment or from a file (default stdin)"""
	if not fp:
		fp = sys.stdin
	if not environ.has_key('REQUEST_METHOD'):
		environ['REQUEST_METHOD'] = 'GET'	# For testing
	if environ['REQUEST_METHOD'] == 'POST':
		ctype, pdict = parse_header(environ['CONTENT_TYPE'])
		if ctype == 'multipart/form-data':
			return parse_multipart(fp, ctype, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			clength = string.atoi(environ['CONTENT_LENGTH'])
			qs = fp.read(clength)
		else:
			qs = ''		# Bad content-type
		environ['QUERY_STRING'] = qs
	elif environ.has_key('QUERY_STRING'):
		qs = environ['QUERY_STRING']
	else:
		if sys.argv[1:]:
			qs = sys.argv[1]
		else:
			qs = ""
		environ['QUERY_STRING'] = qs
	return parse_qs(qs)


def parse_qs(qs):
	"""Parse a query given as a string argument"""
	name_value_pairs = string.splitfields(qs, '&')
	dict = {}
	for name_value in name_value_pairs:
		nv = string.splitfields(name_value, '=')
		if len(nv) != 2:
			continue
		name = nv[0]
		value = urllib.unquote(regsub.gsub('+', ' ', nv[1]))
		if len(value):
			if dict.has_key (name):
				dict[name].append(value)
			else:
				dict[name] = [value]
	return dict


def parse_multipart(fp, ctype, pdict):
	"""Parse multipart input.

	Arguments:
	fp   : input file
	ctype: content-type
	pdict: dictionary containing other parameters of conten-type header

	Returns a dictionary just like parse_qs() (keys are the field
	names, each value is a list of values for that field) except
	that if the value was an uploaded file, it is a tuple of the
	form (filename, content-type, data).  Note that content-type
	is the raw, unparsed contents of the content-type header.

	XXX Should we parse further when the content-type is
	multipart/*?

	"""
	import mimetools
	if pdict.has_key('boundary'):
		boundary = pdict['boundary']
	else:
		boundary = ""
	nextpart = "--" + boundary
	lastpart = "--" + boundary + "--"
	partdict = {}
	terminator = ""

	while terminator != lastpart:
		bytes = -1
		data = None
		if terminator:
			# At start of next part.  Read headers first.
			headers = mimetools.Message(fp)
			clength = headers.getheader('content-length')
			if clength:
				try:
					bytes = string.atoi(clength)
				except string.atoi_error:
					pass
			if bytes > 0:
				data = fp.read(bytes)
			else:
				data = ""
		# Read lines until end of part.
		lines = []
		while 1:
			line = fp.readline()
			if not line:
				terminator = lastpart # End outer loop
				break
			if line[:2] == "--":
				terminator = string.strip(line)
				if terminator in (nextpart, lastpart):
					break
			if line[-2:] == '\r\n':
				line = line[:-2]
			elif line[-1:] == '\n':
				line = line[:-1]
			lines.append(line)
		# Done with part.
		if data is None:
			continue
		if bytes < 0:
			data = string.joinfields(lines, "\n")
		line = headers['content-disposition']
		if not line:
			continue
		key, params = parse_header(line)
		if key != 'form-data':
			continue
		if params.has_key('name'):
			name = params['name']
		else:
			continue
		if params.has_key('filename'):
			data = (params['filename'],
				headers.getheader('content-type'), data)
		if partdict.has_key(name):
			partdict[name].append(data)
		else:
			partdict[name] = [data]

	return partdict


def parse_header(line):
	"""Parse a Content-type like header.
	
	Return the main content-type and a dictionary of options.
	
	"""
	plist = map(string.strip, string.splitfields(line, ';'))
	key = string.lower(plist[0])
	del plist[0]
	pdict = {}
	for p in plist:
		i = string.find(p, '=')
		if i >= 0:
			name = string.lower(string.strip(p[:i]))
			value = string.strip(p[i+1:])
			if len(value) >= 2 and value[0] == value[-1] == '"':
				value = value[1:-1]
			pdict[name] = value
	return key, pdict


# Classes for field storage
# =========================

class MiniFieldStorage:

	"""Internal: dummy FieldStorage, used with query string format."""

	def __init__(self, name, value):
		"""Constructor from field name and value."""
		self.name = name
		self.value = value
		from StringIO import StringIO
		self.filename = None
		self.list = None
		self.file = StringIO(value)

	def __repr__(self):
		"""Return printable representation."""
		return "MiniFieldStorage(%s, %s)" % (`self.name`,
						     `self.value`)


class FieldStorage:

	"""Store a sequence of fields, reading multipart/form-data."""

	def __init__(self, fp=None, headers=None, outerboundary=""):
		"""Constructor.  Read multipart/* until last part."""
		method = None
		if environ.has_key('REQUEST_METHOD'):
			method = string.upper(environ['REQUEST_METHOD'])
		if not fp and method == 'GET':
			qs = None
			if environ.has_key('QUERY_STRING'):
				qs = environ['QUERY_STRING']
			from StringIO import StringIO
			fp = StringIO(qs or "")
			if headers is None:
				headers = {'content-type':
					   "application/x-www-form-urlencoded"}
		if headers is None:
			headers = {}
			if environ.has_key('CONTENT_TYPE'):
				headers['content-type'] = environ['CONTENT_TYPE']
			if environ.has_key('CONTENT_LENGTH'):
				headers['content-length'] = environ['CONTENT_LENGTH']
		self.fp = fp or sys.stdin
		self.headers = headers
		self.outerboundary = outerboundary
		
		# Process content-disposition header
		cdisp, pdict = "", {}
		if self.headers.has_key('content-disposition'):
			cdisp, pdict = parse_header(self.headers['content-disposition'])
		self.disposition = cdisp
		self.disposition_options = pdict
		self.name = None
		if pdict.has_key('name'):
			self.name = pdict['name']
		self.filename = None
		if pdict.has_key('filename'):
			self.filename = pdict['filename']
		
		# Process content-type header
		ctype, pdict = "text/plain", {}
		if self.headers.has_key('content-type'):
			ctype, pdict = parse_header(self.headers['content-type'])
		self.type = ctype
		self.type_options = pdict
		self.innerboundary = ""
		if pdict.has_key('boundary'):
			self.innerboundary = pdict['boundary']
		clen = -1
		if self.headers.has_key('content-length'):
			try:
				clen = string.atoi(self.headers['content-length'])
			except:
				pass
		self.length = clen

		self.list = self.file = None
		self.done = 0
		self.lines = []
		if ctype == 'application/x-www-form-urlencoded':
			self.read_urlencoded()
		elif ctype[:10] == 'multipart/':
			self.read_multi()
		else:
			self.read_single()
	
	def __repr__(self):
		"""Return a printable representation."""
		return "FieldStorage(%s, %s, %s)" % (
			`self.name`, `self.filename`, `self.value`)

	def __getattr__(self, name):
		if name != 'value':
			raise AttributeError, name
		if self.file:
			self.file.seek(0)
			value = self.file.read()
			self.file.seek(0)
		elif self.list is not None:
			value = self.list
		else:
			value = None
		return value
	
	def __getitem__(self, key):
		"""Dictionary style indexing."""
		if self.list is None:
			raise TypeError, "not indexable"
		found = []
		for item in self.list:
			if item.name == key: found.append(item)
		if not found:
			raise KeyError, key
		return found
	
	def keys(self):
		"""Dictionary style keys() method."""
		if self.list is None:
			raise TypeError, "not indexable"
		keys = []
		for item in self.list:
			if item.name not in keys: keys.append(item.name)
		return keys

	def read_urlencoded(self):
		"""Internal: read data in query string format."""
		qs = self.fp.read(self.length)
		dict = parse_qs(qs)
		self.list = []
		for key, valuelist in dict.items():
			for value in valuelist:
				self.list.append(MiniFieldStorage(key, value))
		self.skip_lines()
	
	def read_multi(self):
		"""Internal: read a part that is itself multipart."""
		import rfc822
		self.list = []
		part = self.__class__(self.fp, {}, self.innerboundary)
		# Throw first part away
		while not part.done:
			headers = rfc822.Message(self.fp)
			part = self.__class__(self.fp, headers, self.innerboundary)
			self.list.append(part)
		self.skip_lines()
	
	def read_single(self):
		"""Internal: read an atomic part."""
		if self.length >= 0:
			self.read_binary()
			self.skip_lines()
		else:
			self.read_lines()
		self.file.seek(0)
	
	bufsize = 8*1024		# I/O buffering size for copy to file
	
	def read_binary(self):
		"""Internal: read binary data."""
		self.file = self.make_file('b')
		todo = self.length
		if todo >= 0:
			while todo > 0:
				data = self.fp.read(min(todo, self.bufsize))
				if not data:
					self.done = -1
					break
				self.file.write(data)
				todo = todo - len(data)
	
	def read_lines(self):
		"""Internal: read lines until EOF or outerboundary."""
		self.file = self.make_file('')
		if self.outerboundary:
			self.read_lines_to_outerboundary()
		else:
			self.read_lines_to_eof()
	
	def read_lines_to_eof(self):
		"""Internal: read lines until EOF."""
		while 1:
			line = self.fp.readline()
			if not line:
				self.done = -1
				break
			self.lines.append(line)
			if line[-2:] == '\r\n':
				line = line[:-2] + '\n'
			self.file.write(line)
	
	def read_lines_to_outerboundary(self):
		"""Internal: read lines until outerboundary."""
		next = "--" + self.outerboundary
		last = next + "--"
		delim = ""
		while 1:
			line = self.fp.readline()
			if not line:
				self.done = -1
				break
			self.lines.append(line)
			if line[:2] == "--":
				strippedline = string.strip(line)
				if strippedline == next:
					break
				if strippedline == last:
					self.done = 1
					break
			if line[-2:] == "\r\n":
				line = line[:-2]
			elif line[-1] == "\n":
				line = line[:-1]
			self.file.write(delim + line)
			delim = "\n"
	
	def skip_lines(self):
		"""Internal: skip lines until outer boundary if defined."""
		if not self.outerboundary or self.done:
			return
		next = "--" + self.outerboundary
		last = next + "--"
		while 1:
			line = self.fp.readline()
			if not line:
				self.done = -1
				break
			self.lines.append(line)
			if line[:2] == "--":
				strippedline = string.strip(line)
				if strippedline == next:
					break
				if strippedline == last:
					self.done = 1
					break
	
	def make_file(self, binary):
		"""Overridable: return a readable & writable file.
		
		The file will be used as follows:
		- data is written to it
		- seek(0)
		- data is read from it
		
		The 'binary' argument is 'b' if the file should be created in
		binary mode (on non-Unix systems), '' otherwise.
		
		The intention is that you can override this method to selectively
		create a real (temporary) file or use a memory file dependent on
		the perceived size of the file or the presence of a filename, etc.
		
		"""
		
		# Prefer ArrayIO over StringIO, if it's available
		try:
			from ArrayIO import ArrayIO
			ioclass = ArrayIO
		except ImportError:
			from StringIO import StringIO
			ioclass = StringIO
		return ioclass()


# Main classes
# ============

class FormContentDict:
	"""Basic (multiple values per field) form content as dictionary.
	
	form = FormContentDict()
	
	form[key] -> [value, value, ...]
	form.has_key(key) -> Boolean
	form.keys() -> [key, key, ...]
	form.values() -> [[val, val, ...], [val, val, ...], ...]
	form.items() ->  [(key, [val, val, ...]), (key, [val, val, ...]), ...]
	form.dict == {key: [val, val, ...], ...}

	"""
	def __init__( self ):
		self.dict = parse()
		self.query_string = environ['QUERY_STRING']
	def __getitem__(self,key):
		return self.dict[key]
	def keys(self):
		return self.dict.keys()
	def has_key(self, key):
		return self.dict.has_key(key)
	def values(self):
		return self.dict.values()
	def items(self):
		return self.dict.items() 
	def __len__( self ):
		return len(self.dict)


class SvFormContentDict(FormContentDict):
	"""Strict single-value expecting form content as dictionary.
	
	IF you only expect a single value for each field, then
	form[key] will return that single value.  It will raise an
	IndexError if that expectation is not true.  IF you expect a
	field to have possible multiple values, than you can use
	form.getlist(key) to get all of the values.  values() and
	items() are a compromise: they return single strings where
	there is a single value, and lists of strings otherwise.
	
	"""
	def __getitem__(self, key):
		if len(self.dict[key]) > 1: 
			raise IndexError, 'expecting a single value' 
		return self.dict[key][0]
	def getlist(self, key):
		return self.dict[key]
	def values(self):
		lis = []
		for each in self.dict.values(): 
			if len( each ) == 1 : 
				lis.append(each[0])
			else: lis.append(each)
		return lis
	def items(self):
		lis = []
		for key,value in self.dict.items():
			if len(value) == 1 :
				lis.append((key, value[0]))
			else:	lis.append((key, value))
		return lis


class InterpFormContentDict(SvFormContentDict):
	"""This class is present for backwards compatibility only.""" 
	def __getitem__( self, key ):
		v = SvFormContentDict.__getitem__( self, key )
		if v[0] in string.digits+'+-.' : 
			try:  return  string.atoi( v ) 
			except ValueError:
				try:	return string.atof( v )
				except ValueError: pass
		return string.strip(v)
	def values( self ):
		lis = [] 
		for key in self.keys():
			try:
				lis.append( self[key] )
			except IndexError:
				lis.append( self.dict[key] )
		return lis
	def items( self ):
		lis = [] 
		for key in self.keys():
			try:
				lis.append( (key, self[key]) )
			except IndexError:
				lis.append( (key, self.dict[key]) )
		return lis


class FormContent(FormContentDict):
	"""This class is present for backwards compatibility only.""" 
	def values(self,key):
		if self.dict.has_key(key):return self.dict[key]
		else: return None
	def indexed_value(self,key, location):
		if self.dict.has_key(key):
			if len (self.dict[key]) > location:
				return self.dict[key][location]
			else: return None
		else: return None
	def value(self,key):
		if self.dict.has_key(key):return self.dict[key][0]
		else: return None
	def length(self,key):
		return len (self.dict[key])
	def stripped(self,key):
		if self.dict.has_key(key):return string.strip(self.dict[key][0])
		else: return None
	def pars(self):
		return self.dict


# Test/debug code
# ===============

def test():
	"""Robust test CGI script.
	
	Dump all information provided to the script in HTML form.

	"""
	import traceback
	print "Content-type: text/html"
	print
	sys.stderr = sys.stdout
	try:
		print_environ()
		print_form(FieldStorage())
		print
		print "<H3>Current Working Directory:</H3>"
		try:
			pwd = os.getcwd()
		except os.error, msg:
			print "os.error:", escape(str(msg))
		else:
			print escape(pwd)
		print
	except:
		print "\n\n<PRE>"	# Turn of word wrap
		traceback.print_exc()

def print_environ():
	"""Dump the shell environment in HTML form."""
	keys = environ.keys()
	keys.sort()
	print
	print "<H3>Shell environment:</H3>"
	print "<DL>"
	for key in keys:
		print "<DT>", escape(key), "<DD>", escape(environ[key])
	print "</DL>" 
	print

def print_form(form):
	"""Dump the contents of a form in HTML form."""
	keys = form.keys()
	keys.sort()
	print
	print "<H3>Form contents:</H3>"
	print "<DL>"
	for key in keys:
		print "<DT>" + escape(key) + ":",
		value = form[key]
		print "<i>" + escape(`type(value)`) + "</i>"
		print "<DD>" + escape(`value`)
	print "</DL>"
	print

def print_environ_usage():
	"""Print a list of environment variables used by the CGI protocol."""
	print """
<H3>These environment variables could have been set:</H3>
<UL>
<LI>AUTH_TYPE
<LI>CONTENT_LENGTH
<LI>CONTENT_TYPE
<LI>DATE_GMT
<LI>DATE_LOCAL
<LI>DOCUMENT_NAME
<LI>DOCUMENT_ROOT
<LI>DOCUMENT_URI
<LI>GATEWAY_INTERFACE
<LI>LAST_MODIFIED
<LI>PATH
<LI>PATH_INFO
<LI>PATH_TRANSLATED
<LI>QUERY_STRING
<LI>REMOTE_ADDR
<LI>REMOTE_HOST
<LI>REMOTE_IDENT
<LI>REMOTE_USER
<LI>REQUEST_METHOD
<LI>SCRIPT_NAME
<LI>SERVER_NAME
<LI>SERVER_PORT
<LI>SERVER_PROTOCOL
<LI>SERVER_ROOT
<LI>SERVER_SOFTWARE
</UL>
"""


# Utilities
# =========

def escape(s):
	"""Replace special characters '&', '<' and '>' by SGML entities."""
	s = regsub.gsub("&", "&amp;", s)	# Must be done first!
	s = regsub.gsub("<", "&lt;", s)
	s = regsub.gsub(">", "&gt;", s)
	return s


# Invoke mainline
# ===============

# Call test() when this file is run as a script (not imported as a module)
if __name__ == '__main__': 
	test()
