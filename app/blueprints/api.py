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

from flask import Blueprint, render_template, escape, redirect, url_for, jsonify, make_response,send_file
from flask_login import login_required, current_user
from flask_sqlalchemy import inspect
from sqlalchemy import desc
import subprocess
from datetime import datetime
import os
import shutil
import requests

from app.models.frigate import frigate
from app.models.events import events
from app.models.frigate import frigate
from app.models.cameras import cameras
from app import db
from app.helpers.fetch import Fetch
from app.helpers.cookies import cookies
from app.helpers.iterateQuery import iterateQuery
from app.helpers.logit import logit

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
    if inspect(db.engine).has_table("frigate"):
        db.create_all()
    query = frigate.query.all()
    return iterateQuery(query)

@api.route('/api/events/add/<eventid>/<camera>/<object>/<score>')
@login_required
def apiAddEvent(eventid,camera,score,object):
    source = "fEVR | EVENT ADD"
    time = datetime.fromtimestamp(int(eventid.split('.')[0]))
    # Define default JSON return value
    rVal = {'error':0,
            'msg':'OK',
            'time':time,
            'eventid':eventid,
            'camera':camera,
            'object':object,
            'score':score}
    db.create_all()
    Cameras = cameras.query.filter_by(camera=camera).first()
    if Cameras:
        show = True if Cameras.show else False
        # Check if eventid already exists
        if events.query.filter_by(eventid=eventid).first():
            rVal["msg"] = 'Event Already Exists'
            rVal["error"] = 2
        else: 
            try:
                fetchPath = f"{os.getcwd()}/app/static/events/{eventid}/"
                logit.execute(f"Fetching event into {fetchPath}",src=source)
                frigateConfig = apiFrigate()
                fetched = False
                for frigate in frigateConfig:
                    logit.execute(f"Trying to fetch from {frigateConfig[frigate]['url']}",src=source)
                    frigateURL = frigateConfig[frigate]["url"]
                    Fetched = Fetch(fetchPath,eventid,frigateURL)
                    logit.execute(f"Fetched {Fetched.event}", src=source)
                    fetched = True
                if not fetched:
                    rVal["msg"] = "Cannot Fetch"
                    rVal["error"] = 3
            except Exception as e:
                rVal["error"] = 4
                rVal["msg"] = str(e).replace('"','')
            try:
                event = events(eventid=eventid,camera=camera,object=object,score=int(score),ack='',time=time,show=show)
                db.session.add(event)
                db.session.commit()
            except Exception as e:
                rVal["error"] = 5
                rVal["msg"] = str(e).replace('"','')
    else:
        rVal["msg"] = f"Camera '{camera}' Not Defined"
        rVal["error"] = 1
    return jsonify(rVal)

@api.route('/api/events/ack/<eventid>')
@login_required
def apiAckEvent(eventid):
    try:
        query = events.query.filter_by(eventid=eventid).first()
        query.ack = "true"
        db.session.commit()
        rVal = {'msg': 'Success'}
    except:
        rVal = {'error': 1, 'msg': 'Failed'}
    return jsonify(rVal)

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
    Cameras = cameras.query.all()
    cookiejar = {}
    cookiejar['menu'] = cookies.getCookie('menu') if cookies.getCookie('menu') else "closed"
    cookiejar['page'] = cookies.getCookie('page') if cookies.getCookie('page') else "/"
    cookiejar['cameras'] = str(Cameras)
    events.query.filter_by(eventid=eventid).delete()
    # Delete Event Files if they exist
    eventPath = f"{os.getcwd()}/app/static/events/{eventid}"
    if os.path.exists(eventPath):
        shutil.rmtree(eventPath)
    db.session.commit()
    return redirect(cookiejar['page'])

@api.route('/api/events/latest')
@login_required
def apiShowLatest():
    if not inspect(db.engine).has_table("events"):
        db.create_all()
    query = events.query.order_by(desc(events.time)).limit(12).all()
    return iterateQuery(query)

@api.route('/api/events/all')
@login_required
def apiShowAllEvents():
    if not inspect(db.engine).has_table("events"):
        db.create_all()
    query = events.query.order_by(desc(events.time)).all()
    return iterateQuery(query)

@api.route('/api/event/<eventid>')
@login_required
def apiSingleEvent(eventid):
    query = events.query.filter_by(eventid=eventid)
    return iterateQuery(query)

@api.route('/api/event/clip/<eventid>')
def apiEventClip(eventid):
    clip = f"{os.getcwd()}/app/static/events/{eventid}/clip.mp4"
    try:
        return send_file(clip,attachment_filename="clip.mp4")
    except Exception as error:
        return jsonify({"error": error})
            

@api.route('/api/events/camera/<camera>')
@login_required
def apiEventsByCamera(camera):
    query = events.query.filter_by(camera=camera)
    return iterateQuery(query)

@api.route('/api/cameras/add/<camera>/<server>/<show>')
@login_required
def apiAddCamera(camera,server,show):
    db.create_all()
    hls = f"http://{server}:5084/{camera}"
    rtsp = f"rtsp://{server}:5082/{camera}"
    show = True if show == "true" or show == "True" else False
    camera = cameras(camera=camera,hls=hls,rtsp=rtsp,show=show)
    db.session.add(camera)
    db.session.commit()
    return jsonify({'msg': 'Camera Added Successfully'})

@api.route('/api/cameras/<camera>')
@login_required
def apiCameras(camera):
    if not inspect(db.engine).has_table("cameras"):
        db.create_all()
    if camera == "all":
        query = cameras.query.all()
    else:
        query = cameras.query.filter_by(camera=camera)
    return iterateQuery(query)

@api.route('/api/cameras/<camera>/snapshot/<height>')
@login_required
def apiSnapshot(camera,height):
    frigateConfig = apiFrigate()
    snapshot = None
    for frigate in frigateConfig:
        try:
            snapshot = requests.get(f"{frigateConfig[frigate]['url']}/api/{camera}/latest.jpg?height={height}", allow_redirects=True).content
            with open(f'/tmp/{camera}.jpg','wb') as snap:
                snap.write(snapshot)
            return send_file(f'/tmp/{camera}.jpg',attachment_filename="snapshot.jpg")
        except Exception as error:
            return jsonify({"error": error})