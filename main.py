#!/usr/bin/env python3
import elf

path = "/home/amitsa/JNI-Obfuscator/example/bin/"
l = elf.ELF()

l.append_lib(path + 'libb.so')
l.append_lib(path + 'liba.so')

l.replace_symbols([path + 'main', path + 'liba.so', path + 'libb.so'])