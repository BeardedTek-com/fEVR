#!/usr/bin/python
def main():
    print("content-type: text/html\n\n")
    print("<html><head><title>fEVR debug log</title><link rel='stylesheet' href='/css/logs.css'/></head><body><div class='logfile'><pre><code>")
    with open("/var/www/logs/debug.log","r") as logfile:
        print(logfile.read())
    print("</code></pre></div></body></html>")

main()