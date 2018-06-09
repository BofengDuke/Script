#!/bin/bash

# Install shadowsocks for ubuntu
# description: Shadows start/stop/status/restart/install script
# Usage: ./shadowsocks_init.sh {start|stop|status|restart|install}

shadowsocks_bin=`which ssserver`
shadowsocks_conf=/etc/shadowsocks/config.json
shadowsocks_usage="Usage: $0 {\e[00;32mstart\e[00m|\e[00;31mstop\e[00m|\e[00;32mstatus\e[00m|\e[00;31mrestart\e[00m|\e[00;32minstall\e[00m}"


shadowsocks_pid(){
    echo `ps -ef | grep $shadowsocks_bin | grep -v grep | tr -s " "|cut -d" " -f2`
}


install(){
    echo "Input your passwd: "
    read passwd
	echo -e  "\e[00;32mwaiting ......\e[00m"


    apt-get update &>/dev/null 
    apt-get install python-pip - &>/dev/null
    python -m pip install --upgrade pip &>/dev/null
    python -m pip install shadowsocks &>/dev/null

    mkdir -p /etc/shadowsocks/

    CONFIG=" {\n
        \"server\":\"0.0.0.0\",\n
        \"server_port\":8388,\n
        \"local_address\":\"127.0.0.1\",\n
        \"local_port\":1088,\n
        \"password\":\"$passwd\",\n
        \"timeout\":600,\n
        \"method\":\"aes-256-cfb\",\n
        \"fast_open\": false,\n
        \"workers\": 1,\n
        \"prefer_ipv6\": false\n
     }"
    echo -e  $CONFIG > $shadowsocks_conf
    
	echo -e "\n------------------------------------"
    echo "Install success,your base info is:"
    echo -e  "Config file:\e[00;32m $shadowsocks_conf\e[00m"
    echo "You can check your configuration in config file."
    echo -e "Now,you can start ss by: \e[00;32m$0 start\e[00m\n"

}

start(){
    pid=$(shadowsocks_pid)
    if [ -n "$pid" ];then
        echo -e "\e[00;31mShadowsocks is already running (pid: $pid)\e[00m"
    else
        $shadowsocks_bin -c $shadowsocks_conf -d start
        RETVAL=$?
        if [ "$RETVAL" = "0" ];then
            echo -e "\e[00;32mStarting Shadowsocks\e[00m"
        else 
            echo -e "\e[00;32mShadowsocks start Failed\e[00m"
        fi
        status
    fi
    return 0
}

status(){
    pid=$(shadowsocks_pid)
    if [ -n "$pid" ];then
        echo -e "\e[00;32mShadowsocks is running with pid: $pid\e[00m"
    else
        echo -e "\e[00;31mShadowsocks is not running\e[00m"
    fi
}

stop(){
    pid=$(shadowsocks_pid)
    if [ -n "$pid" ];then
        echo -e "\e[00;31mStoping Shadowsocks\e[00m"
		$shadowsocks_bin -c $shadowsocks_conf -d stop
	else
    	echo -e "\e[00;31mShadowsocks is not running\e[00m"
	fi
	
	return 0
}

case $1 in
	start)
		start
	;;
	stop)
		stop
	;;
	restart)
		stop
		start
	;;
	status)
		status
	;;
	install)
		install
	;;
	*)
	echo -e $shadowsocks_usage
esac
exit 0




