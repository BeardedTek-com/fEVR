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

from flask import Blueprint, render_template, redirect, url_for, make_response, flash, request
from flask_login import login_required
from sqlalchemy import desc

from app.models.cameras import cameras
from app.models.events import events
from app.models.frigate import frigate
import app.blueprints.api as api
from app.helpers.cookies import cookies
from app.helpers.logit import logit
from app import db


main = Blueprint('main',__name__)

# Main Routes
@main.route('/', defaults={'currentPage': 1})
@main.route('/latest', defaults={'currentPage': 1})
@main.route('/all', defaults={'currentPage': 1})
@main.route('/<int:currentPage>')
@login_required
def viewAll(currentPage):
    Cameras = cameras.query.all()
    cookiejar = {}
    cookiejar['menu'] = cookies.getCookie('menu') if cookies.getCookie('menu') else "closed"
    LastPage = cookies.getCookie('page') if cookies.getCookie('page') else "/"
    cookiejar['page'] = request.path
    cookiejar['count'] = cookies.getCookie('count') if cookies.getCookie('count') else "50"
    perPage = int(cookiejar['count'])
    cookiejar['cameras'] = str(Cameras)
    title=f"Events"
    Events = events.query.filter(events.show==True).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
    perPage = int(cookiejar['count'])
    nextPage = url_for('main.viewAll',currentPage=Events.next_num) if Events.has_next else None
    prevPage = url_for('main.viewAll',currentPage=Events.prev_num) if Events.has_prev else None
    Pages = {
        "page": currentPage,
        "prevURL": prevPage,
        "nextURL": nextPage,
        "pageCount": Events.pages,
        "eventCount": Events.total,
        "perPage": perPage
    }
    resp = make_response(render_template('events.html',Menu=cookiejar['menu'],page=LastPage,title=title,events=Events.items,cameras=Cameras,Pages=Pages,camera="all"))
    for cookie in cookiejar:
            resp.set_cookie(cookie,cookiejar[cookie])
    return resp

@main.route('/events/camera/<Camera>', defaults={'currentPage': 1})
@main.route('/events/camera/<Camera>/<int:currentPage>')
@login_required
def viewEventsbyCamera(Camera,currentPage):
    Cameras = cameras.query.all()
    cookiejar = {}
    cookiejar['menu'] = cookies.getCookie('menu') if cookies.getCookie('menu') else "closed"
    LastPage = cookies.getCookie('page') if cookies.getCookie('page') else "/"
    cookiejar['page'] = request.path
    cookiejar['count'] = cookies.getCookie('count') if cookies.getCookie('count') else "50"
    perPage = int(cookiejar['count'])
    cookiejar['cameras'] = str(Cameras)
    title=f"{Camera.title()} Events"
    Events = events.query.filter(events.camera==Camera).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
    perPage = int(cookiejar['count'])
    nextPage = url_for('main.viewEventsbyCamera',currentPage=Events.next_num,Camera=Camera) if Events.has_next else None
    prevPage = url_for('main.viewEventsbyCamera',currentPage=Events.prev_num,Camera=Camera) if Events.has_prev else None
    Pages = {
        "page": currentPage,
        "prevURL": prevPage,
        "nextURL": nextPage,
        "pageCount": Events.pages,
        "eventCount": Events.total,
        "perPage": perPage
    }
    resp = make_response(render_template('events.html',Menu=cookiejar['menu'],page=LastPage,title=title,events=Events.items,cameras=Cameras,camera=Camera,Pages=Pages))
    for cookie in cookiejar:
            resp.set_cookie(cookie,cookiejar[cookie])
    return resp

@main.route('/events/camera/<Camera>/<filter>/<value>', defaults={'currentPage': 1})
@main.route('/events/camera/<Camera>/<filter>/<value>/<int:currentPage>')
@login_required
def viewEventsbyCameraFiltered(Camera,filter,value,currentPage):
    Cameras = cameras.query.all()
    cookiejar = {}
    cookiejar['menu'] = cookies.getCookie('menu') if cookies.getCookie('menu') else "closed"
    LastPage = cookies.getCookie('page') if cookies.getCookie('page') else request.path
    cookiejar['page'] = request.path
    cookiejar['count'] = cookies.getCookie('count') if cookies.getCookie('count') else "50"
    perPage = int(cookiejar['count'])
    cookiejar['cameras'] = str(Cameras)
    if request.cookies.get('menu'):
        menu = request.cookies.get('menu')
    else:
        menu = 'closed'
    cookiejar['menu'] = menu
    validFilter = False
    validValue = False
    validFilters = {'object':
                        ['car','animal','person'],
                    'score':
                        [60,100],
                    'ack':
                        ['true','false']
                    }
    for fil in validFilters:
        if filter == fil:
            validFilter = True
            if filter == 'score':
                if validFilters[fil][0] <= int(value) <= validFilters[fil][0]:
                    validValue = True
            else:
                for val in validFilters[fil]:
                    if val == value:
                        validValue = True
    if validFilter and validValue:
        title=f"{Camera.title()} Events by {value.title()}"
        if Camera == "all":
            if filter == 'object':
                Events = events.query.filter(events.object==value,events.show==True).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
            if filter == 'score':
                Events = events.query.filter(events.score==int(value),events.show==True).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
            if filter == 'ack':
                value = "" if value == "false" else value
                Events = events.query.filter(events.ack==value,events.show==True).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
        else:
            if filter == 'object':
                Events = events.query.filter(events.camera==Camera,events.object==value).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
            if filter == 'score':
                Events = events.query.filter(events.camera==Camera,events.score==int(value)).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
            if filter == 'ack':
                value = "" if value == "false" else value
                Events = events.query.filter(events.camera==Camera,events.ack==value).order_by(desc(events.time)).paginate(currentPage,perPage,error_out=False)
    else:
        flashMessage = f"Invalid filter selected. Valid filters are:"
        for fil in validFilters:
            flashMessage += f" {fil}"
        flashMessage+= "."
        flash(flashMessage)
    perPage = int(cookiejar['count'])
    nextPage = url_for('main.viewAll',currentPage=Events.next_num) if Events.has_next else None
    prevPage = url_for('main.viewAll',currentPage=Events.prev_num) if Events.has_prev else None
    Pages = {
        "page": currentPage,
        "prevURL": prevPage,
        "nextURL": nextPage,
        "pageCount": Events.pages,
        "eventCount": Events.total,
        "perPage": perPage
    }
    resp = make_response(render_template('events.html',Menu=cookiejar['menu'],page=LastPage,title=title,events=Events.items,cameras=Cameras,Pages=Pages,camera=Camera))
    for cookie in cookiejar:
            resp.set_cookie(cookie,cookiejar[cookie])
    return resp

@main.route('/event/<eventid>/<view>')
@login_required
def viewSingle(eventid,view):
    cookiejar = {}
    Cameras = cameras.query.all()
    cookiejar['menu'] = request.cookies.get('menu') if request.cookies.get('menu') else "closed"
    LastPage = request.cookies.get('page') if request.cookies.get('page') else "/"
    cookiejar['page'] = request.path if not 'del' in request.path else LastPage
    cookiejar['cameras'] = str(Cameras)
    Frigate = frigate.query.first()
    try: 
        frigateURL = Frigate['url']
    except:
        frigateURL = "http://frigate:5000"
    if view == 'ack':
        api.apiAckEvent(eventid)
    elif view == 'unack':
        api.apiUnackEvent(eventid)
    elif view == 'delOK':
        api.apiDelEvent(eventid)
        if cookiejar.get('page'):
            fwd = cookiejar['page']
        else:
            fwd = "/"
        resp = redirect(fwd)

    event = events.query.filter_by(eventid=eventid).first()
    if event:
        if event.ack == "" and view != 'unack':
            event.ack = "true"
            db.session.commit()
        resp = make_response(render_template('event.html',Menu=cookiejar['menu'],page=LastPage,event=event,view=view,frigateURL=frigateURL,cameras=Cameras))
    else:
        if cookiejar.get('page'):
            fwd = cookiejar['page']
        else:
            fwd = "/"
        resp = redirect(fwd)
    return cookies.setCookies(cookiejar,resp)

    
