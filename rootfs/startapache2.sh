#!/bin/bash
if ! $(ps | grep -v grep | grep -q httpd); then
    echo "apache2 not running. starting...";
    httpd;
fi