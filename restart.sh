#!/bin/bash
echo "--===Restart module starting===--"


PID0=`ps aux | awk '/buy.py/ && !/awk/ { print $2 }'`
echo "$PID0"
if [ "$PID0" ]
then
        echo "Process exists, lets kill it"
        kill $PID0
else
        echo "Process absent, moving to other process"
fi




PID1=`ps aux | awk '/sell.py/ && !/awk/ { print $2 }'`
echo "$PID1"
if [ "$PID1" ]
then
        echo "Process exists, lets kill it"
        kill $PID1
else
        echo "Process absent, moving to other process"
fi




#PID2=`ps aux | awk '/server.py/ && !/awk/ { print $2 }'`
#kill -9 $PID2


#PID22=`ps aux | awk '/server.py/ && !/awk/ { print $2 }'`
#kill -9 $PID22



PID3=`ps aux | awk '/neuralprediction.py/ && !/awk/ { print $2 }'`
echo "$PID3"
if [ "$PID3" ]
then
        echo "Process exists, lets kill it"
        kill $PID3
else
        echo "Process absent, moving to other process"
fi





PID4=`ps aux | awk '/heikin_ashi.py/ && !/awk/ { print $2 }'`
echo "$PID4"
if [ "$PID4" ]
then
        echo "Process exists, lets kill it"
        kill $PID4
else
        echo "Process absent, moving to other process"
fi



PID5=`ps aux | awk '/enable_market.py/ && !/awk/ { print $2 }'`
echo "$PID5"
if [ "$PID5" ]
then
        echo "Process exists, lets kill it"
        kill $PID5
else
        echo "Process absent, moving to other process"
fi




PID6=`ps aux | awk '/heikin_day.py/ && !/awk/ { print $2 }'`
echo "$PID6"
if [ "$PID6" ]
then
        echo "Process exists, lets kill it"
        kill $PID6
else
        echo "Process absent, moving to other process"
fi




PID7=`ps aux | awk '/chart_creator.py/ && !/awk/ { print $2 }'`
echo "$PID7"
if [ "$PID7" ]
then
        echo "Process exists, lets kill it"
        kill $PID7
else
        echo "Process absent, moving to other process"
fi




PID8=`ps aux | awk '/chart_creator2.py/ && !/awk/ { print $2 }'`
echo "$PID8"
if [ "$PID8" ]
then
        echo "Process exists, lets kill it"
        kill $PID8
else
        echo "Process absent, moving to other process"
fi




PID9=`ps aux | awk '/check_market_profits.py/ && !/awk/ { print $2 }'`
echo "$PID9"
if [ "$PID9" ]
then
        echo "Process exists, lets kill it"
        kill $PID9
else
        echo "Process absent, moving to other process"
fi





PID10=`ps aux | awk '/btc_ha.py/ && !/awk/ { print $2 }'`
echo "$PID10"
if [ "$PID10" ]
then
        echo "Process exists, lets kill it"
        kill $PID10
else
        echo "Process absent, moving to other process"
fi



PID11=`ps aux | awk '/chart_creator3.py/ && !/awk/ { print $2 }'`
echo "$PID11"
if [ "$PID11" ]
then
        echo "Process exists, lets kill it"
        kill $PID11
else
        echo "Process absent, moving to other process"
fi




PID12=`ps aux | awk '/check_ai.py/ && !/awk/ { print $2 }'`
echo "$PID12"
if [ "$PID12" ]
then
        echo "Process exists, lets kill it"
        kill $PID12
else
        echo "Process absent, moving to other process"
fi




PID13=`ps aux | awk '/aftercount.py/ && !/awk/ { print $2 }'`
echo "$PID13"
if [ "$PID13" ]
then
        echo "Process exists, lets kill it"
        kill $PID13
else
        echo "Process absent, moving to other process"
fi




PID14=`ps aux | awk '/chart_creator4.py/ && !/awk/ { print $2 }'`
echo "$PID14"
if [ "$PID14" ]
then
        echo "Process exists, lets kill it"
        kill $PID14
else
        echo "Process absent, moving to other process"
fi




PID15=`ps aux | awk '/statistic.py/ && !/awk/ { print $2 }'`
echo "$PID15"
if [ "$PID15" ]
then
        echo "Process exists, lets kill it"
        kill $PID15
else
        echo "Process absent, moving to other process"
fi




#PID16=`ps aux | awk '/btc_status.py/ && !/awk/ { print $2 }'`
#kill -9 $PID16

PID17=`ps aux | awk '/candles.py/ && !/awk/ { print $2 }'`
echo "$PID17"
if [ "$PID17" ]
then
        echo "Process exists, lets kill it"
        kill $PID17
else
        echo "Process absent, moving to other process"
fi




PID18=`ps aux | awk '/check_candle_signals.py/ && !/awk/ { print $2 }'`
echo "$PID18"
if [ "$PID18" ]
then
        echo "Process exists, lets kill it"
        kill $PID18
else
        echo "Process absent, moving to other process"
fi




PID19=`ps aux | awk '/chart_creator5.py/ && !/awk/ { print $2 }'`
echo "$PID19"
if [ "$PID19" ]
then
        echo "Process exists, lets kill it"
        kill $PID19
else
        echo "Process absent, moving to other process"
fi



PID20=`ps aux | awk '/score.py/ && !/awk/ { print $2 }'`
echo "$PID20"
if [ "$PID20" ]
then
        echo "Process exists, lets kill it"
        kill $PID20
else
        echo "Process absent, moving to other process"
fi






PID21=`ps aux | awk '/order_counts.py/ && !/awk/ { print $2 }'`
echo "$PID21"
if [ "$PID21" ]
then
        echo "Process exists, lets kill it"
        kill $PID21
else
        echo "Process absent, moving to other process"
fi




PID22=`ps aux | awk '/stat.py/ && !/awk/ { print $2 }'`
echo "$PID22"
if [ "$PID22" ]
then
        echo "Process exists, lets kill it"
        kill $PID22
else
        echo "Process absent, moving to other process"
fi


PID23=`ps aux | awk '/grow_percent.py/ && !/awk/ { print $2 }'`
echo "$PID23"
if [ "$PID23" ]
then
        echo "Process exists, lets kill it"
        kill $PID23
else
        echo "Process absent, moving to other process"
fi


PID24=`ps aux | awk '/price_tracker.py/ && !/awk/ { print $2 }'`
echo "$PID24"
if [ "$PID24" ]
then
        echo "Process exists, lets kill it"
        kill $PID24
else
        echo "Process absent, moving to other process"
fi





