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
import svgwrite
class drawSVG:
    svg = {
        'text':'fEVR',
        'stroke':'none',
        'insert':(0,20),
        'fill':'#000000',
        'font':{
            'family':'Arial',
            'size':'20px',
            'weight':'bold'
            }
    }
    def toString(svg=svg):
        dwg = svgwrite.Drawing('test2.svg', profile='tiny')
        dwg.add(dwg.text(svg['text'],
                        insert=svg['insert'],
                        stroke=svg['stroke'],
                        fill=svg['fill'],
                        font_size=svg['font']['size'],
                        font_weight=svg['font']['weight'],
                        font_family=svg['font']['family'])
                )
        return dwg.tostring()