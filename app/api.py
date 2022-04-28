from flask import Blueprint, render_template, escape, redirect, url_for, jsonify, make_response
from flask_login import login_required, current_user
from sqlalchemy import desc
import subprocess
from datetime import datetime
import os


from .models.models import events,frigate,cameras
from . import db
from .fetch import Fetch
from .helpers.cookies import cookies

# API Routes
api = Blueprint('api',__name__)

@api.route('/routes')
@login_required
def apiHome():
    Cookies = cookies.getCookies(['menu','page'])
    cookiejar = {'page':'/'}
    title = "fEVR API Routes"
    routes = subprocess.Popen("flask routes", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
    contents = "<div class='routes'>"
    contents += f"<div class='routes-title'><span class='method'>Method</span> <span>Path</span></div>\n"
    for count, line in enumerate(routes.split("\n")):
        if count > 2:
            method = line[29:36]
            link = line[38:].replace('<','&#60;').replace('>','&#62;')
            if (count % 2) == 0:
                contents += "<div class='routes-odd'>"
            else:
                contents += "<div class='routes-even'>"
            contents += f"<span class='method'>{method}</span> <span><a href='{link}'>{link}</a></span>\n"
            contents += "</div>"
    contents += "</div>"
    resp = render_template('api.html',menu=Cookies['menu'],page='/routes',title=title, contents=contents)
    return cookies.setCookies(cookiejar,make_response(resp))

@api.route('/api/frigate/add/<name>/<http>/<ip>/<port>')
def apiAddFrigate(name,http,ip,port):
    db.create_all()
    url = f"{http}://{ip}:{port}/"
    Frigate = frigate(name=name,url=url)
    db.session.add(Frigate)
    db.session.commit()
    return jsonify({'name':escape(name),'url':escape(url)})

@api.route('/api/frigate')
def apiFrigate():
    if frigate.exists():
        db.create_all()
    query = frigate.query.all()
    internal = ""
    external = ""
    for Frigate in query:
        if Frigate.name == "frigate":
            internal = Frigate.url
        if Frigate.name == "external":
            external = Frigate.url
    if not internal:
        internal = "http://frigate.local:5000/"
    if not external:
        external = internal
    return {'frigate':f"{internal}/",'external':f"{external}/"}

@api.route('/api/events/add/<eventid>/<camera>/<object>/<score>')
@login_required
def apiAddEvent(eventid,camera,score,object):
    def addEvent(eventid,camera,score,object):
        db.create_all()
        time = datetime.fromtimestamp(int(eventid.split('.')[0]))
        event = events(eventid=eventid,camera=camera,object=object,score=int(score),ack='',time=time)
        db.session.add(event)
        db.session.commit()
        fetchPath = f"{os.getcwd()}/app/static/events/{eventid}/"
        frigateConfig = apiFrigate()
        frigateURL = frigateConfig['frigate']
        
        print(f"######################################################################################### \n \
                # Fetching {eventid} for {object} in {camera} from {frigateConfig['frigate']} \n \
                ######################################################################################### ")
        Fetch(fetchPath,eventid,frigateURL)
        
    # Check if eventid already exists
    if events.query.filter_by(eventid=eventid).first():
        return jsonify({'msg':'Event Already Exists'})
    # Are they authorized?
#    elif apiAuth.exe():
    else:
        addEvent(eventid,camera,score,object)
        return jsonify({'msg':'Success'})
#    else:
#        return 'Not Authorized', 200
@api.route('/api/admin/events/add/<eventid>/<camera>/<object>/<score>')
@login_required
def apiAdminAddEvent(eventid,camera,score,object):
    def addEvent(eventid,camera,score,object):
        db.create_all()
        time = datetime.fromtimestamp(int(eventid.split('.')[0]))
        event = events(eventid=eventid,camera=camera,object=object,score=int(score),ack='',time=time)
        db.session.add(event)
        db.session.commit()
        fetchPath = f"{os.getcwd()}/app/static/events/{eventid}/"
        frigateConfig = apiFrigate()
        frigateURL = frigateConfig['frigate']
        
        print(f"######################################################################################### \n \
                # Fetching {eventid} for {object} in {camera} from {frigateConfig['frigate']} \n \
                ######################################################################################### ")
        Fetch(fetchPath,eventid,frigateURL)
    if current_user.group == 'admin':
        addEvent(eventid,camera,score,object)
        return jsonify({'msg': 'Success'})
    else:
        return jsonify({'msg': 'Not Authorized'})

@api.route('/api/events/ack/<eventid>')
@login_required
def apiAckEvent(eventid):
    query = events.query.filter_by(eventid=eventid).first()
    query.ack = "true"
    db.session.commit()
    return jsonify({'msg': 'Success'})

@api.route('/api/events/unack/<eventid>')
@login_required
def apiUnackEvent(eventid):
    query = events.query.filter_by(eventid=eventid).first()
    query.ack = ""
    db.session.commit()
    return jsonify({'msg':'Success'})

@api.route('/api/events/del/<eventid>')
@login_required
def apiDelEvent(eventid):
    events.query.filter_by(eventid=eventid).delete()
    db.session.commit()
    return redirect(url_for('main.index'))

@api.route('/api/events/latest')
@login_required
def apiShowLatest():
    if not events.exists():
        db.create_all()
    query = events.query.order_by(desc(events.time)).limit(12).all()
    return events.dict(query)

@api.route('/api/events/all')
@login_required
def apiShowAllEvents():
    if not events.exists():
        db.create_all()
    query = events.query.order_by(desc(events.time)).all()
    return events.dict(query)

@api.route('/api/event/<eventid>/<view>')
@login_required
def apiSingleEvent(eventid):
    query = events.query.filter_by(eventid=eventid)
    return events.dict(query)

@api.route('/api/events/camera/<camera>')
@login_required
def apiEventsByCamera(camera):
    query = events.query.filter_by(camera=camera)
    return events.dict(query)

@api.route('/api/cameras/add/<camera>/<server>')
@login_required
def apiAddCamera(camera,server):
    db.create_all()
    hls = f"http://{server}:5084/{camera}"
    rtsp = f"rtsp://{server}:5082/{camera}"
    camera = cameras(camera=camera,hls=hls,rtsp=rtsp)
    db.session.add(camera)
    db.session.commit()
    return jsonify({'msg': 'Camera Added Successfully'})

@api.route('/api/cameras/<camera>')
@login_required
def apiCameras(camera):
    if not cameras.exists():
        db.create_all()
    if camera == "all":
        query = cameras.query.all()
    else:
        query = cameras.query.filter_by(camera=camera)
    return cameras.dict(query)