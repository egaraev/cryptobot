#!/bin/bash
for i in `ps -ef | grep -v grep | grep start.sh | awk '{print $2}'`; do kill $i; done
