#!/usr/bin/sh

mkdir rpn/docs
pydoc -m `find ./rpn -name '*.py'`
mv *.html rpn/docs
