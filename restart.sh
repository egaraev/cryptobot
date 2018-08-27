#!/bin/bash

SERVICE1='main.py'

PID1=`ps aux | awk '/main.py/ && !/awk/ { print $2 }'`

kill -9 $PID1

SERVICE2='server.py'

PID2=`ps aux | awk '/server.py/ && !/awk/ { print $2 }'`

kill -9 $PID2

SERVICE3='neuralprediction.py'

PID3=`ps aux | awk '/neuralprediction.py/ && !/awk/ { print $2 }'`

kill -9 $PID3

SERVICE4='heikin_ashi.py'

PID4=`ps aux | awk '/heikin_ashi.py/ && !/awk/ { print $2 }'`

kill -9 $PID4

PID5=`ps aux | awk '/enable_market.py/ && !/awk/ { print $2 }'`

kill -9 $PID5

PID6=`ps aux | awk '/heikin_day.py/ && !/awk/ { print $2 }'`

kill -9 $PID6

