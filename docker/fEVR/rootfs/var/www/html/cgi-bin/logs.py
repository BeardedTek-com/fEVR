#!/usr/bin/python
#    fEVR (frigate Event Video Recorder)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
class displog:
    def __init__(self):
        import cgi
        self.input = cgi.FieldStorage()
        self.type = self.input.getvalue('type')
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
    def displayLog(self):
        print("content-type: text/html\n\n")
        print("<html><head><title>fEVR debug log</title><link rel='stylesheet' href='..//css/logs.css'/></head><body><div class='logfile'><pre><code>")
        logpath = f"/var/www/logs/"
        logfile = f"{self.type}.log"
        self.error.execute(f"Displaying {logfile}",src=self.script)
        with open(f"{logpath}{logfile}","r") as logFile:
            print(logFile.read())
        print("</code></pre></div></body></html>")

def main():
    dispLog = displog()
    dispLog.displayLog()

main()