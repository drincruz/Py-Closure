#!/usr/bin/evn python


"""
Python client for the Closure Compiler Service
http://closure-compiler.appspot.com/home

"""

import argparse
import httplib
import json
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
            required=True
        )
    args = parser.parse_args()

    print(_compile(args.file, args.compilation))

def _compile(filename, compilation):
    """
    Handle the minification tasks

    Keyword arguments:
    filename - Filename path of the file to minify
    compilation_level - Compilation levels accepted by Closure
    """
    # Read in the file to minify
    with open(filename, 'rb') as f:
        _JS = f.read()

    # Try and compile, check for errors
    closure_return = json.loads(_closure(
            _JS,
            compilation,
            'json',
            'errors')
        )

    # Check for errors
    if 'errors' in closure_return:
        sys.stderr.write("[ERROR] %s\n" % (closure_return['errors']))
        sys.exit(1)
    else:
        # Try and compile, check for errors
        compiled_js = _closure(
                _JS,
                compilation,
                'text',
                'compiled_code'
            )

        return compiled_js

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

if '__main__' == __name__:
    main()
