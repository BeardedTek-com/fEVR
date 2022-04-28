
from time import time
import sys

class logit:
    def execute(msg,src='fEVR',debug=True):
        def to_stderr(*a):
            print(*a, file=sys.stderr)
        logtime = "{:.4f}".format(time())
        logentry = f"{logtime} {str(msg)}"
        if debug:
            to_stderr(f"[ {src:15}] {logentry}")
