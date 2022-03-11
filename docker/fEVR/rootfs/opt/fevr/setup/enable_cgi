#!/bin/bash

# MPM (if MPM=event is specified, use it, else use "prefork" as default)
case "${HTTPD_MPM:=event}" in
   prefork) ;;
   worker)  sed -i -e '/LoadModule mpm_worker/s/^#//' \
                   -e '/LoadModule mpm_prefork/s/^/#/' \
                    /etc/apache2/httpd.conf
            ;;
   event)   sed -i -e '/LoadModule mpm_event/s/^#//' \
                   -e '/LoadModule mpm_prefork/s/^/#/' \
                    /etc/apache2/httpd.conf
            ;;
   *)       echo "Err: MPM should be 'event' or 'prefork', not '$MPM'"
            exit 1
esac


# Make Apache tuning on default httpd.conf
sed -i -e '/LoadModule slotmem_shm_module/s/^#//' \
       -e '/ErrorLog.*error.log/s,logs.*$,"|/usr/sbin/rotatelogs -l -f -c /var/log/apache2/error-%m%d.log 86400",' \
       -e '/CustomLog.*access.log/s,logs/access.log,"|/usr/sbin/rotatelogs -l -f -c /var/log/apache2/access-%m%d.log 86400",' \
       -e '/Options Indexes FollowSymLinks/s/$/ ExecCGI/' \
       /etc/apache2/httpd.conf

# Activate CGI if HTTPD_ENABLE_CGI is true
[ "${HTTPD_ENABLE_CGI:=true}" == true ] && \
sed -i -e '/index\.html$/s/$/ index.sh index.cgi/' \
       -e '/LoadModule cgi/s/#//' \
       -e '/Scriptsock cgisock/s/#//' \
       -e '/AddHandler cgi-script .cgi/s/#//' -e '/AddHandler cgi-script .cgi/s/$/ .sh .py/' \
       -e '/Options Indexes FollowSymLinks/s/$/ ExecCGI/' /etc/apache2/httpd.conf

# Move DocumentRoot to /var/www/html
sed -i -e 's,/var/www/localhost/htdocs,/var/www/html,' /etc/apache2/httpd.conf


mkdir -p /run/apache2
cat <<DONE > /etc/supervisord.conf
[supervisord]
user=root
nodaemon=true              ; (start in foreground if true;default false)
logfile=/var/log/supervisord.log  ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=50MB       ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10          ; (num of main logfile rotation backups;default 10)
loglevel=info               ; (log level;default info; others: debug,warn,trace)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)

[program:httpd]
command=/usr/sbin/httpd -DFOREGROUND

DONE

echo "Going-on with MPM ${HTTPD_MPM}, ENABLE_CGI is ${HTTPD_ENABLE_CGI}."
exec "$@"
