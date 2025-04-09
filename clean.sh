#!/bin/bash

# Threshold size in bytes (1 KB = 1024 bytes)
SIZE_THRESHOLD=200024

# Find and remove files smaller than 1 KB
find . -type f -size -"$SIZE_THRESHOLD"c -exec rm -v {} \;

# Explanation:
# - . : Search in current directory
# - -type f : Only match regular files (not directories)
# - -size -1024c : Match files smaller than 1024 bytes (- means less than, c means bytes)
# - -exec rm -v {} \; : Remove matched files (-v for verbose output)
