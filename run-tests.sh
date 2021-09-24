#!/bin/sh

tput reset
python3 -m unittest discover ./rpn/test
