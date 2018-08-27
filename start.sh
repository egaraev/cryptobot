#!/bin/bash

SERVICE1='main.py'
 
if ps ax | grep -v grep | grep $SERVICE1 > /dev/null
then
    echo "$SERVICE1 service running "
else
    echo there is no such "$SERVICE1 service, starting"
    /usr/bin/python2.7 /root/PycharmProjects/cryptobot/main.py
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
#/usr/bin/python2.7 /root/PycharmProjects/cryptobot/heikin_ashi.py

fi


SERVICE6='heikin_day.py'

if ps ax | grep -v grep | grep $SERVICE6 > /dev/null
then
    echo "$SERVICE5 service running "
else
    echo there is no such "$SERVICE6 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 heikin_day.py
#/usr/bin/python2.7 /root/PycharmProjects/cryptobot/heikin_day.py

fi

