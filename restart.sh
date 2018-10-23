#!/bin/bash

PID1=`ps aux | awk '/main.py/ && !/awk/ { print $2 }'`
kill -9 $PID1


PID2=`ps aux | awk '/server.py/ && !/awk/ { print $2 }'`
kill -9 $PID2


PID3=`ps aux | awk '/neuralprediction.py/ && !/awk/ { print $2 }'`
kill -9 $PID3


PID4=`ps aux | awk '/heikin_ashi.py/ && !/awk/ { print $2 }'`
kill -9 $PID4


PID5=`ps aux | awk '/enable_market.py/ && !/awk/ { print $2 }'`
kill -9 $PID5


PID6=`ps aux | awk '/heikin_day.py/ && !/awk/ { print $2 }'`
kill -9 $PID6


PID7=`ps aux | awk '/chart_creator.py/ && !/awk/ { print $2 }'`
kill -9 $PID7


PID8=`ps aux | awk '/chart_creator2.py/ && !/awk/ { print $2 }'`
kill -9 $PID8


PID9=`ps aux | awk '/check_market_profits.py/ && !/awk/ { print $2 }'`
kill -9 $PID9

PID10=`ps aux | awk '/btc_ha.py/ && !/awk/ { print $2 }'`
kill -9 $PID10

