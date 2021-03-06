#!/usr/bin/env python


"""
Python client for the Closure Compiler Service
http://closure-compiler.appspot.com/home

"""

__version__ = '0.1.1'

import argparse
import httplib
import json
import os
import sys

from urllib import urlencode


def main():
    """
    Main

    """
    parser = argparse.ArgumentParser(
            description="A command-line interface for Closure compiler")
    parser.add_argument(
            '-c',
            '--compilation',
            default='WHITESPACE_ONLY',
            help='Compilation type: WHITESPACE_ONLY, SIMPLE_OPTIMIZATIONS, ADVANCED_OPTIMIZATIONS',
            required=False
        )
    parser.add_argument(
            '-f',
            '--file',
            help='Filename of js we want to compile',
            required=True
        )
    parser.add_argument(
            '-o',
            '--outfile',
            help='Filename to save the compiled js to',
            required=False
        )
    parser.add_argument(
            '-m',
            '--minify',
            help='Minify the js',
            action="store_true"
        )
    parser.add_argument(
            '-e',
            '--error_check',
            help='Check the js for compilation errors',
            action="store_true"
        )
    args = parser.parse_args()

    # Read in the file to minify
    with open(args.file, 'rb') as f:
        _JS = f.read()


    if args.error_check:
        # Check the js for compilation errors first
        if False == _error_check(_JS, args.compilation):
            sys.exit(1)

        # Exit after error check success
        sys.stdout.write("%s compiled successfully.\n" % args.file)
        sys.exit(0)
    else:
        # Default to just minifying
        sys.stdout.write("Compiling %s...\n" % args.file)
        minified_js = _compile(_JS, args.compilation)

    sys.stdout.write("Writing minified file...\n")

    if args.outfile:
        _writefile(args.outfile, minified_js)
    else:
        _writefile(_min_filename(args.file), minified_js)

    sys.exit(0)

def _compile(js, compilation):
    """
    Handle the minification tasks

    Keyword arguments:
    js - Javascript to minify
    compilation_level - Compilation levels accepted by Closure
    """

    # Compile
    compiled_js = _closure(
            js,
            compilation,
            'text',
            'compiled_code'
        )

    return compiled_js

def _error_check(js, compilation):
    """
    Check for any errors in compiling

    Keyword arguments:
    js - Javascript to check for errors
    compilation - Compilation levels accepted by Closure
    """
    # Try and compile, check for errors
    closure_return = json.loads(_closure(
            js,
            compilation,
            'json',
            'errors')
        )

    # Check for errors
    if 'errors' in closure_return:
        sys.stderr.write("[ERROR] %s\n" % (closure_return['errors']))
        return False
    else:
        return True

def _closure(
        js,
        comp_level='WHITESPACE_ONLY',
        output='text',
        output_type='compiled_code'):
    """
    Process the REST call to Closure

    Keyword arguments:
    js - Javascript to minify
    comp_level - Compilation options: WHITESPACE_ONLY, SIMPLE_OPTIMIZATIONS, ADVANCED_OPTIMIZATIONS
    output - The output returned format: text, json, xml
    output_type - The type of data returned: compiled_code, warnings, errors, statistics
    """

    _CLOSURE = 'closure-compiler.appspot.com'
    _CLOSURE_COMPILER = '/compile'

    data = (
            ('js_code', js),
            ('compilation_level', comp_level),
            ('output_format', output),
            ('output_info', output_type)
        )
    headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }

    conn = httplib.HTTPConnection(_CLOSURE)
    conn.request('POST', _CLOSURE_COMPILER, urlencode(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def _min_filename(filename):
    """
    Get the minified js filename

    Keyword arguments:
    filename - The js filename
    """
    filename_parts = os.path.splitext(filename)
    return filename_parts[0] + '.min' + filename_parts[1]

def _writefile(outfile, minjs):
    """
    Write the minified js to a file

    Keyword arguments:
    outfile - The output filename
    minjs - The minified js
    """
    with open(outfile, 'wb') as f:
        f.write(minjs)


if '__main__' == __name__:
    main()
