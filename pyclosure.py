#!/usr/bin/evn python


"""
Python client for the Closure Compiler Service
http://closure-compiler.appspot.com/home

"""

import argparse
import httplib

from urllib import urlencode


def main():
    """
    Main

    """
    parser = argparse.ArgumentParser(
            description="A command-line interface for Closure compiler")
    parser.add_argument('-c', '--compilation', required=False)
    parser.add_argument('-f', '--file', required=True)
    args = parser.parse_args()

    _compile(args.file, args.compilation)

def _compile(filename, compilation_level=None):
    """
    Handle the minification tasks

    Keyword arguments:
    filename - Filename path of the file to minify
    compilation_level - Compilation levels accepted by Closure
    """
    _CLOSURE = 'closure-compiler.appspot.com'
    _CLOSURE_COMPILER = '/compile'

    # Read in the file to minify
    with open(filename, 'rb') as f:
        _JS = f.read()

    # Set the compilation level (WHITESPACE_ONLY, SIMPLE_OPTIMIZATIONS, ADVANCED_OPTIMIZATIONS)
    if None == compilation_level:
        _COMP_LEVEL = 'WHITESPACE_ONLY'
    else:
        _COMP_LEVEL = compilation_level

    data = (
            ('js_code', _JS),
            ('compilation_level', _COMP_LEVEL),
            ('output_format', 'json'),
            ('output_info', 'compiled_code')
        )
    headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }

    conn = httplib.HTTPConnection(_CLOSURE)
    conn.request('POST', _CLOSURE_COMPILER, urlencode(data), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()

if '__main__' == __name__:
    main()
