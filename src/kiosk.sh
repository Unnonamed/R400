#!/bin/bash
## 디스플레이 지정 필요 line 6
## 화면꺼짐 방지 line 21~23
## 마우스 숨기기 line 25 apt-get install unclutter
#
export DISPLAY=":0"

PGM_NAME=chrome
DATE=`date +%Y%m%d-%H%M%S`

Cnt=`ps -ef|grep $PGM_NAME|grep -v grep|grep -v vi|wc -l`
PROCESS=`ps -ef|grep $PGM_NAME|grep -v grep|grep -v vi|awk '{print $2}'`

echo "$Cnt : $DATE :: $PGM_NAME (PID : $PROCESS) is now running."

#while true;
#do
if [ $Cnt -eq 0 ]; then 

        echo "$Cnt : $DATE :: $PGM_NAME (PID : $PROCESS) is now running."

        xset s off
        set -dpms
        xset s noblank
        chromium-browser --kiosk -disable-translate --noerrdialogs /media/pi/USB%20드라이브/colorbar.mp4
        unclutter -idle 0
        echo hi

else
        echo "$DATE : $PGM_NAME is not running."
fi
#done
echo "exit program"
