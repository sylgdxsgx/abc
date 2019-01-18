#!/bin/bash
savepath=$(cd `dirname $0`; pwd)
function pause(){
        read -n 1 -p "$*" INP
        if [ [$INP != ''] ] ; then
                echo -ne '\b \n'
                echo $INP
        fi
}
deviceNames=""
function split_arr(){
	x=$1

	# OLD_IFS="$IFS"
	# IFS="\n\n"
	# array=($x)
	# IFS="$OLD_IFS"

	# echo ${array}
	# for each in ${array[*]}
	# do
	#     echo $each
	#     deviceNames=$each
	# done
	
	echo $x | awk '{split($0,arr," ");for(i in arr) print i,arr[i]}'
	# return ${array[*]}
}
adb wait-for-device
echo 'wait-for-device'
adb devices

# result=`adb devices`
# echo "$result"
# echo ${#result}
# split_arr "$result"
# echo $deviceNames
# ipAddr=${result#*attached}
# ipAddr=${ipAddr%%device*}
# ipAddr=${ipAddr:2:19}
# echo $ipAddr
read -p "please enter device name:" ipAddr
# pause 'Press any key to continue...'
while true; 
do
	pause 'Note: 1 for scrrenrecord other for screenshot:'
	DATE=`date +%Y%m%d%H%M%S`
	fileName=$DATE

	if [ [$INP = '1'] ]; then
		fileName="screen_"$fileName".mp4"
		echo ${fileName}
		adb -s ${ipAddr} shell screenrecord /sdcard/${fileName}
	else
		fileName="screen_"$fileName".png"
		echo ${fileName}
		adb -s ${ipAddr} shell screencap ./sdcard/${fileName} 
	fi
	adb -s ${ipAddr} pull ./sdcard/${fileName} ${savepath}
	adb -s ${ipAddr} shell rm ./sdcard/${fileName} 
	echo "save ${fileName} to ${savepath} success!"
	echo -ne '\b \n'
done
