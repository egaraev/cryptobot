
 SERVICE24='price_tracker.py'

 if ps ax | grep -v grep | grep $SERVICE24 > /dev/null
 then
     echo "$SERVICE24 service running "
 else
     echo there is no such "$SERVICE24 service, starting"
     cd /root/PycharmProjects/cryptobot
     stdbuf -oL /usr/bin/python2.7 price_tracker.py >> /root/price_tracker

 fi