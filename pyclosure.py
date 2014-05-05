#!/usr/bin/evn python


"""
Python client for the Closure Compiler Service
http://closure-compiler.appspot.com/home

"""

import httplib 
import urllib

from urllib import urlencode


def main():
    """
    Main

    """

    _CLOSURE = 'closure-compiler.appspot.com'
    _CLOSURE_COMPILER = '/compile'

    data = (
            ('js_code', 'alert("oh hai there");'),
            ('compilation_level', 'WHITESPACE_ONLY'),
            ('output_format', 'json'),
            ('output_info', 'compiled_code')
        )
    headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }

    conn = httplib.HTTPConnection(_CLOSURE)
    conn.request('POST', _CLOSURE_COMPILER, urlencode(data), headers)
    print(conn)
    response = conn.getresponse()
    print(response)
    data = response.read()
    print(data)
    conn.close()

if '__main__' == __name__:
    main()
