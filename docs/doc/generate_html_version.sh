#!/bin/bash
make clean

filename="getting_started.rst"

# store the original version of $filename
cp "${filename}" "${filename}.orig"

# replace all :download: directives
sed -i '/(:download:.*/ {N; s/(:download:`.*`)//g}' "${filename}"

make latexpdf

# restore original $filename
cp "${filename}".orig "${filename}"

rm "${filename}".orig
