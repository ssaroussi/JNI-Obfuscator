#!/usr/bin/env python3
import lief

class Inserter:
    symbols = []

    def append_lib(self, f_path):
        binary = lief.parse(f_path)
        print(dir(binary))

    def __init__(self):
        # Retrive from the symbols file
        pass

    def __del__(self):
        # Save the symbols in a file
        pass

def replace_symbols():
    pass
