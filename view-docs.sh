#!/bin/sh
export DOCS_DIR=./rpn/docs
export TARGET_DIR=./rpn/src

if [ ! -d "$DOCS_DIR" ]; then
    mkdir "$DOCS_DIR"
fi
pydoc -m "find $TARGET_DIR -name '*.py'"
mv ./*.html rpn/docs

cd "$DOCS_DIR" || exit
python3 -m http.server 9876 -b 127.0.0.1

