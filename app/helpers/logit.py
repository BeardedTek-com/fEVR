#    This code is a portion of frigate Event Video Recorder (fEVR)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU AfferoGeneral Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from time import time
import sys

class logit:
    def execute(msg,src='fEVR',debug=True):
        def to_stderr(*a):
            print(*a, file=sys.stderr)
        logtime = "{:.2f}".format(time())
        logentry = f"{logtime} {str(msg)}"
        if debug:
            to_stderr(f"[ {src:16} ] {logentry}")
