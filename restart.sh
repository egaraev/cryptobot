#!/bin/bash

#PID1=`ps aux | awk '/main.py/ && !/awk/ { print $2 }'`
#kill -9 $PID1


PID0=`ps aux | awk '/buy.py/ && !/awk/ { print $2 }'`
kill  $PID0


PID1=`ps aux | awk '/sell.py/ && !/awk/ { print $2 }'`
kill  $PID1




#PID2=`ps aux | awk '/server.py/ && !/awk/ { print $2 }'`
#kill -9 $PID2


#PID22=`ps aux | awk '/server.py/ && !/awk/ { print $2 }'`
#kill -9 $PID22



PID3=`ps aux | awk '/neuralprediction.py/ && !/awk/ { print $2 }'`
kill  $PID3


PID4=`ps aux | awk '/heikin_ashi.py/ && !/awk/ { print $2 }'`
kill  $PID4


PID5=`ps aux | awk '/enable_market.py/ && !/awk/ { print $2 }'`
kill  $PID5


PID6=`ps aux | awk '/heikin_day.py/ && !/awk/ { print $2 }'`
kill  $PID6


PID7=`ps aux | awk '/chart_creator.py/ && !/awk/ { print $2 }'`
kill  $PID7


PID8=`ps aux | awk '/chart_creator2.py/ && !/awk/ { print $2 }'`
kill  $PID8


PID9=`ps aux | awk '/check_market_profits.py/ && !/awk/ { print $2 }'`
kill  $PID9

#PID10=`ps aux | awk '/btc_ha.py/ && !/awk/ { print $2 }'`
#kill  $PID10


PID11=`ps aux | awk '/chart_creator3.py/ && !/awk/ { print $2 }'`
kill  $PID11


PID12=`ps aux | awk '/check_ai.py/ && !/awk/ { print $2 }'`
kill  $PID12


PID13=`ps aux | awk '/aftercount.py/ && !/awk/ { print $2 }'`
kill  $PID13


PID14=`ps aux | awk '/chart_creator4.py/ && !/awk/ { print $2 }'`
kill  $PID14


PID15=`ps aux | awk '/statistic.py/ && !/awk/ { print $2 }'`
kill  $PID15


#PID16=`ps aux | awk '/btc_status.py/ && !/awk/ { print $2 }'`
#kill -9 $PID16

PID17=`ps aux | awk '/candles.py/ && !/awk/ { print $2 }'`
kill  $PID17


PID18=`ps aux | awk '/check_candle_signals.py/ && !/awk/ { print $2 }'`
kill  $PID18

PID19=`ps aux | awk '/chart_creator5.py/ && !/awk/ { print $2 }'`
kill  $PID19

PID20=`ps aux | awk '/score.py/ && !/awk/ { print $2 }'`
kill  $PID20

PID21=`ps aux | awk '/order_counts.py/ && !/awk/ { print $2 }'`
kill  $PID21


PID22=`ps aux | awk '/stat.py/ && !/awk/ { print $2 }'`
kill  $PID22


