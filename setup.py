import sys

from cx_Freeze import setup, Executable

#if you want to use py2exe for making exacutable windows file.

setup(  name = "pygraph",

        version = "1.0",

        description = "drawing math graph program",

        author = "soori",

        executables = [Executable("pygraph.py")])        