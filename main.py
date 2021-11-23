#!/usr/bin/python3
import sys

try:
    name_file = sys.argv[1]
    print(name_file)
except :
    print("Veuillez preciser le PDF")
