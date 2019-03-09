#!/bin/bash

#SERVICE1='main.py'
 
#if ps ax | grep -v grep | grep $SERVICE1 > /dev/null
#then
#    echo "$SERVICE1 service running "
#else
#    echo there is no such "$SERVICE1 service, starting"
#    /usr/bin/python2.7 /root/PycharmProjects/cryptobot/main.py
#fi


SERVICE0='buy.py'

if ps ax | grep -v grep | grep $SERVICE0 > /dev/null
then
    echo "$SERVICE0 service running "
else
    echo there is no such "$SERVICE0 service, starting"
    /usr/bin/python2.7 /root/PycharmProjects/cryptobot/buy.py
fi



SERVICE1='sell.py'

if ps ax | grep -v grep | grep $SERVICE1 > /dev/null
then
    echo "$SERVICE1 service running "
else
    echo there is no such "$SERVICE1 service, starting"
    /usr/bin/python2.7 /root/PycharmProjects/cryptobot/sell.py
fi







SERVICE2='server.py'

if ps ax | grep -v grep | grep $SERVICE2 > /dev/null
then
    echo "$SERVICE2 service running "
else
    echo there is no such "$SERVICE2 service, starting"
    /usr/bin/python2.7 /root/PycharmProjects/cryptobot/webinterface/server.py
fi


SERVICE3='neuralprediction.py'

if ps ax | grep -v grep | grep $SERVICE3 > /dev/null
then
    echo "$SERVICE3 service running "
else
    echo there is no such "$SERVICE3 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 neuralprediction.py 
#/usr/bin/python2.7 /root/PycharmProjects/cryptobot/neuralprediction.py

fi


SERVICE4='heikin_ashi.py'

if ps ax | grep -v grep | grep $SERVICE4 > /dev/null
then
    echo "$SERVICE4 service running "
else
    echo there is no such "$SERVICE4 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 heikin_ashi.py
#/usr/bin/python2.7 /root/PycharmProjects/cryptobot/heikin_ashi.py

fi


SERVICE5='enable_market.py'

if ps ax | grep -v grep | grep $SERVICE5 > /dev/null
then
    echo "$SERVICE5 service running "
else
    echo there is no such "$SERVICE5 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 enable_market.py

fi


SERVICE6='heikin_day.py'

if ps ax | grep -v grep | grep $SERVICE6 > /dev/null
then
    echo "$SERVICE6 service running "
else
    echo there is no such "$SERVICE6 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 heikin_day.py

fi


SERVICE7='chart_creator.py'

if ps ax | grep -v grep | grep $SERVICE7 > /dev/null
then
    echo "$SERVICE7 service running "
else
    echo there is no such "$SERVICE7 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 chart_creator.py

fi



SERVICE8='check_market_profits.py'

if ps ax | grep -v grep | grep $SERVICE8 > /dev/null
then
    echo "$SERVICE8 service running "
else
    echo there is no such "$SERVICE8 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 check_market_profits.py

fi


SERVICE9='chart_creator2.py'

if ps ax | grep -v grep | grep $SERVICE9 > /dev/null
then
    echo "$SERVICE9 service running "
else
    echo there is no such "$SERVICE9 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 chart_creator2.py

fi


SERVICE10='btc_ha.py'

if ps ax | grep -v grep | grep $SERVICE10 > /dev/null
then
    echo "$SERVICE10 service running "
else
    echo there is no such "$SERVICE10 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 btc_ha.py

fi




SERVICE11='check_ai.py'

if ps ax | grep -v grep | grep $SERVICE11 > /dev/null
then
    echo "$SERVICE11 service running "
else
    echo there is no such "$SERVICE8 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 check_ai.py

fi


SERVICE12='chart_creator3.py'

if ps ax | grep -v grep | grep $SERVICE12 > /dev/null
then
    echo "$SERVICE12 service running "
else
    echo there is no such "$SERVICE12 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 chart_creator3.py

fi

SERVICE13='aftercount.py'

if ps ax | grep -v grep | grep $SERVICE13 > /dev/null
then
    echo "$SERVICE13 service running "
else
    echo there is no such "$SERVICE13 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 aftercount.py

fi


SERVICE14='chart_creator4.py'

if ps ax | grep -v grep | grep $SERVICE14 > /dev/null
then
    echo "$SERVICE14 service running "
else
    echo there is no such "$SERVICE14 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 chart_creator4.py

fi


SERVICE15='statistic.py'

if ps ax | grep -v grep | grep $SERVICE15 > /dev/null
then
    echo "$SERVICE15 service running "
else
    echo there is no such "$SERVICE15 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 statistic.py

fi


SERVICE16='btc_status.py'

if ps ax | grep -v grep | grep $SERVICE16 > /dev/null
then
    echo "$SERVICE16 service running "
else
    echo there is no such "$SERVICE16 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 btc_status.py

fi


SERVICE17='candles.py'

if ps ax | grep -v grep | grep $SERVICE17 > /dev/null
then
    echo "$SERVICE17 service running "
else
    echo there is no such "$SERVICE17 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 candles.py

fi





SERVICE18='check_candle_signals.py'

if ps ax | grep -v grep | grep $SERVICE18 > /dev/null
then
    echo "$SERVICE18 service running "
else
    echo there is no such "$SERVICE18 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 check_candle_signals.py

fi



SERVICE19='chart_creator5.py'

if ps ax | grep -v grep | grep $SERVICE19 > /dev/null
then
    echo "$SERVICE19 service running "
else
    echo there is no such "$SERVICE19 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 chart_creator5.py

fi




SERVICE20='score.py'

if ps ax | grep -v grep | grep $SERVICE20 > /dev/null
then
    echo "$SERVICE20 service running "
else
    echo there is no such "$SERVICE20 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 score.py

fi

