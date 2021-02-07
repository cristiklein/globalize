#!/usr/bin/env python3

import os
import sys

from globalize.globalize import globalize

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} input.jpg")
    raise SystemExit()

inputFilename = sys.argv[1]
basePath, baseExt = os.path.splitext(inputFilename)
outputFilename = basePath + '-globalized' + baseExt

print(f"Globalizing {inputFilename} to {outputFilename}")
globalize(inputFilename, outputFilename)
