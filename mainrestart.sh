PID0=`ps aux | awk '/buy.py/ && !/awk/ { print $2 }'`
kill -9 $PID0


PID1=`ps aux | awk '/sell.py/ && !/awk/ { print $2 }'`
kill -9 $PID1

PID2=`ps aux | awk '/sentiment.py/ && !/awk/ { print $2 }'`
kill -9 $PID2

