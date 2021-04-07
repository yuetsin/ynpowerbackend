#!/usr/bin/env bash

killall gunicorn

rm out.log
rm error.log

gunicorn -w 2 -b :18000 app:app 1>>out.log 2>>error.log &