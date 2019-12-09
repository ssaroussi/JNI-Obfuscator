#!/usr/bin/env python3
from lief import parse
from dill import load, dump

import hashlib
from atexit import register
from os import path, makedirs
from ntpath import basename
from typing import Set
from dataclasses import dataclass
import name_generator

@dataclass
class Symbol:
    mangled_name: str
    demangled_name: str

    def __hash__(self):
        return hash((self.mangled_name, self.demangled_name))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Symbol):
            return False

        return self.mangled_name == other.mangled_name and \
            self.demangled_name == other.demangled_name


class ELF():
    _symbols: Set[Symbol] = set()
    _symbols_path = "symbols.dlill"
    _hashed_binaries_path = "hashed/"
    
    def __init__(self):
        register(self.on_exit)
        self.retrive()

    def append_lib(self, f_path: str):
        binary = parse(f_path)
        self._symbols |= set([Symbol(sym.name, sym.demangled_name)
                             for sym in binary.dynamic_symbols if sym.value != 0])


    def replace_symbols(self, f_paths: Set[str]):
        def generate_hashed_symbols:
            excluded_symbol_hashes: Set[set] = set()
            symbols: Dict[str, str] = dict()
            
            for symbol in self._symbols:
                hashed_name = name_generator.most_similar(symbol.demangled_name, excluded_symbol_hashes)
                symbols[symbol.mangled_name] = hashed_name
                excluded_symbol_hashes.add(hashed_name)

            return symbols

        if not path.exists(self._hashed_binaries_path):
            makedirs(self._hashed_binaries_path)

        for f_path in f_paths:
            binary = parse(f_path)

            find_symbol_by_name = lambda name: \
                next(filter(lambda e : e.name == name, binary.dynamic_symbols), None)

            # Consuse symbols
            for symbol_name, symbol_hash in generate_hashed_symbols():
                symbol_obj = find_symbol_by_name(symbol_name)
                if symbol_obj is not None:
                    symbol_obj.name = symbol_hash
            
            # Write changes to the binary
            binary.write(path.join(self._hashed_binaries_path, basename(f_path)))

    def store(self):
        dump(self._symbols, open(self._symbols_path, "wb"))

    def retrive(self) -> Set[Symbol]:
        try:
            self._symbols = load(open(self._symbols_path, "rb"))
        except FileNotFoundError:
            self._symbols = set()

    def on_exit(self):
        self.store()
