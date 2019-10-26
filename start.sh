#!/bin/bash

SERVICE0='buy.py'

if ps ax | grep -v grep | grep $SERVICE0 > /dev/null
then
    echo "$SERVICE0 service running "
else
    echo there is no such "$SERVICE0 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 buy.py &
fi



SERVICE1='sell.py'

if ps ax | grep -v grep | grep $SERVICE1 > /dev/null
then
    echo "$SERVICE1 service running "
else
    echo there is no such "$SERVICE1 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 sell.py &
fi


#++++
#SERVICE2='server.py'

#if ps ax | grep -v grep | grep $SERVICE2 > /dev/null
#then
#    echo "$SERVICE2 service running "
#else
#    echo there is no such "$SERVICE2 service, starting"
#    /usr/bin/python2.7 /root/PycharmProjects/cryptobot/webinterface/server.py
#fi
#+++++

SERVICE3='neuralprediction.py'

if ps ax | grep -v grep | grep $SERVICE3 > /dev/null
then
    echo "$SERVICE3 service running "
else
    echo there is no such "$SERVICE3 service, starting"
    cd /root/PycharmProjects/cryptobot
    /usr/bin/python2.7 neuralprediction.py 
fi


#SERVICE4='heikin_ashi.py'

#if ps ax | grep -v grep | grep $SERVICE4 > /dev/null
#then
#    echo "$SERVICE4 service running "
#else
#    echo there is no such "$SERVICE4 service, starting"
#    cd /root/PycharmProjects/cryptobot
#    /usr/bin/python2.7 heikin_ashi.py &

#fi


#SERVICE5='enable_market.py'

#if ps ax | grep -v grep | grep $SERVICE5 > /dev/null
#then
#    echo "$SERVICE5 service running "
#else
#    echo there is no such "$SERVICE5 service, starting"
#    cd /root/PycharmProjects/cryptobot
#    /usr/bin/python2.7 enable_market.py &

#fi


#SERVICE6='heikin_day.py'

#if ps ax | grep -v grep | grep $SERVICE6 > /dev/null
#then
#    echo "$SERVICE6 service running "
#else
#    echo there is no such "$SERVICE6 service, starting"
#    cd /root/PycharmProjects/cryptobot
#    /usr/bin/python2.7 heikin_day.py &

#fi









#SERVICE10='btc_ha.py'

# if ps ax | grep -v grep | grep $SERVICE10 > /dev/null
# then
#     echo "$SERVICE10 service running "
# else
#     echo there is no such "$SERVICE10 service, starting"
#     cd /root/PycharmProjects/cryptobot
#     /usr/bin/python2.7 btc_ha.py

# fi





# SERVICE13='aftercount.py'

# if ps ax | grep -v grep | grep $SERVICE13 > /dev/null
# then
#     echo "$SERVICE13 service running "
# else
#     echo there is no such "$SERVICE13 service, starting"
#     cd /root/PycharmProjects/cryptobot
#     /usr/bin/python2.7 aftercount.py &

# fi





#SERVICE16='btc_status.py'

#if ps ax | grep -v grep | grep $SERVICE16 > /dev/null
#then
#    echo "$SERVICE16 service running "
#else
#    echo there is no such "$SERVICE16 service, starting"
#    cd /root/PycharmProjects/cryptobot
#    /usr/bin/python2.7 btc_status.py

#fi


 SERVICE17='candles.py'

 if ps ax | grep -v grep | grep $SERVICE17 > /dev/null
 then
     echo "$SERVICE17 service running "
 else
     echo there is no such "$SERVICE17 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 candles.py &

 fi










 SERVICE20='score.py'

 if ps ax | grep -v grep | grep $SERVICE20 > /dev/null
 then
     echo "$SERVICE20 service running "
 else
     echo there is no such "$SERVICE20 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 score.py &

 fi




# SERVICE21='order_counts.py'

# if ps ax | grep -v grep | grep $SERVICE21 > /dev/null
# then
#     echo "$SERVICE21 service running "
# else
#     echo there is no such "$SERVICE21 service, starting"
#     cd /root/PycharmProjects/cryptobot
#     /usr/bin/python2.7 order_counts.py &

# fi




 SERVICE22='stat.py'

 if ps ax | grep -v grep | grep $SERVICE22 > /dev/null
 then
     echo "$SERVICE22 service running "
 else
     echo there is no such "$SERVICE22 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 stat.py &

 fi


 SERVICE23='grow_percent.py'

 if ps ax | grep -v grep | grep $SERVICE23 > /dev/null
 then
     echo "$SERVICE23 service running "
 else
     echo there is no such "$SERVICE23 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 grow_percent.py &

 fi


