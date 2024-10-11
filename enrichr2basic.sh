#!/bin/bash

cat $1 | awk -F, '{diff=NF-10; printf "%s,%s", $1,$2 ; for (i=3; i<=3+diff;i++) printf $i; print$(NF-1)}' | sed -e 's/""/","/g'
