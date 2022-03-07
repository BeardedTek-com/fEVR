#!/usr/bin/python
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