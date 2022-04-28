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