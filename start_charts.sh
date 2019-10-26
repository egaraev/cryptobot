#!/bin/bash

SERVICE7='chart_creator.py'

if ps ax | grep -v grep | grep $SERVICE7 > /dev/null
then
    echo "$SERVICE7 service running "
else
    echo there is no such "$SERVICE7 service, starting"
     cd /root/PycharmProjects/cryptobot
         /usr/bin/python2.7 chart_creator.py &

fi

 SERVICE8='check_market_profits.py'

 if ps ax | grep -v grep | grep $SERVICE8 > /dev/null
 then
     echo "$SERVICE8 service running "
 else
     echo there is no such "$SERVICE8 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 check_market_profits.py &

 fi


 SERVICE9='chart_creator2.py'

 if ps ax | grep -v grep | grep $SERVICE9 > /dev/null
 then
     echo "$SERVICE9 service running "
 else
     echo there is no such "$SERVICE9 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 chart_creator2.py &

 fi
 
 
 SERVICE11='check_ai.py'

 if ps ax | grep -v grep | grep $SERVICE11 > /dev/null
 then
     echo "$SERVICE11 service running "
 else
     echo there is no such "$SERVICE8 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 check_ai.py &

fi


 SERVICE12='chart_creator3.py'

 if ps ax | grep -v grep | grep $SERVICE12 > /dev/null
 then
     echo "$SERVICE12 service running "
 else
     echo there is no such "$SERVICE12 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 chart_creator3.py &

 fi
 

SERVICE14='chart_creator4.py'

 if ps ax | grep -v grep | grep $SERVICE14 > /dev/null
 then
     echo "$SERVICE14 service running "
 else
     echo there is no such "$SERVICE14 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 chart_creator4.py &

 fi


 SERVICE15='statistic.py'

 if ps ax | grep -v grep | grep $SERVICE15 > /dev/null
 then
     echo "$SERVICE15 service running "
 else
     echo there is no such "$SERVICE15 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 statistic.py &

 fi
 
 SERVICE18='check_candle_signals.py'

 if ps ax | grep -v grep | grep $SERVICE18 > /dev/null
 then
     echo "$SERVICE18 service running "
 else
     echo there is no such "$SERVICE18 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 check_candle_signals.py &
 fi



 SERVICE19='chart_creator5.py'

 if ps ax | grep -v grep | grep $SERVICE19 > /dev/null
 then
     echo "$SERVICE19 service running "
 else
     echo there is no such "$SERVICE19 service, starting"
     cd /root/PycharmProjects/cryptobot
     /usr/bin/python2.7 chart_creator5.py &

 fi
 
 
