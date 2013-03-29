#!/bin/bash
pgrep -x qstardict 1>/dev/null 2>/dev/null
if [ $? -eq 0 ];then
    qdbus org.qstardict.dbus /qstardict org.freedesktop.DBus.Properties.Set \
        org.qstardict.dbus mainWindowVisible 1 1>/dev/null 2>/dev/null
else
    qstardict &
    qdbus org.qstardict.dbus /qstardict org.freedesktop.DBus.Properties.Set \
        org.qstardict.dbus mainWindowVisible 1 1>/dev/null 2>/dev/null
fi
