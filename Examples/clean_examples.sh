#!/bin/bash
# find all result* directories and delete them
find . -name "result*" -type d -exec rm -r {} \;
