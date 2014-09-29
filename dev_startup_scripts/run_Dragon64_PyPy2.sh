#!/bin/bash

# https://github.com/jedie/PyDragon32/tree/master/misc#readme

(
    set -x
    ~/pypy2/bin/pypy ../DragonPy_CLI.py --verbosity=30 --machine=Dragon64 run
)
echo
read -n1 -p "Start bash? [y,n]" doit
echo
case $doit in
    y|Y)
        bash -i
        exit 0
        ;;
    n|N)
        echo "bye bye"
        ;;
    *)
        echo "input, don't know, bye."
        ;;
esac