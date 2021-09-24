#!/usr/bin/sh

mkdir rpn/docs
pydoc -m `find ./rpn -name '*.py'`
mv *.html rpn/docs

cd rpn/docs
python3 -m http.server 9876 -b 127.0.0.1

