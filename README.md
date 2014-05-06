Py-Closure
==========

Python client for Closure Compiler Service
http://closure-compiler.appspot.com/home


Do you use Closure Compiler? Well, I do and I needed a way to automate 
my minification tasks. Automating for me requires a command line utility 
to handle these tasks; so, that's what this project is!


## Basic Usage

Create a .min.js file.
This example will create a '/path/to/yourjsfile.min.js' file.

```
python pyclosure.py -f /path/to/yourjsfile.js
```

Create a .min.js to a file that you specify.
This example will create a '/tmp/different.min.js' file.

```
python pyclosure.py --file=/path/to/yourjsfile.js --outfile=/tmp/different.min.js
```
