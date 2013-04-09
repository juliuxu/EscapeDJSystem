#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJDIR=$DIR
PIDFILE="$PROJDIR/escapedjsystem.pid"
SOCKET="$PROJDIR/escapedjsystem.sock"

function stop_djangoapp {
	if [ -f $PIDFILE ]; then
	    kill `cat -- $PIDFILE`
	    rm -f -- $PIDFILE
	fi
}

function start_djangoapp {
	cd $PROJDIR
	python manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE 
}

case "$1" in
	start)
		echo "Starting django app"
		start_djangoapp
	;;

	stop)
		echo "Stopping django app"
		stop_djangoapp
	;;

	restart)
		$0 stop
		sleep 1
		$0 start
	;;
	*)
		echo "Usage: $0 {start|stop|restart}"
	;;

esac

exit 0
