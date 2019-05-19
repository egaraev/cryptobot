PID0=`ps aux | awk '/buy.py/ && !/awk/ { print $2 }'`
kill $PID0


PID1=`ps aux | awk '/sell.py/ && !/awk/ { print $2 }'`
kill $PID1

PID2=`ps aux | awk '/sentiment.py/ && !/awk/ { print $2 }'`
kill $PID2

