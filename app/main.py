from flask import Blueprint, render_template, redirect, url_for, make_response, flash, request
from flask_login import login_required
from sqlalchemy import desc
from .models.models import frigate, cameras, events, User, apiAuth, config
from . import api
from .helpers.cookies import cookies
from .logit import logit
from . import db
main = Blueprint('main',__name__)


# Main Routes
@main.route('/')
@login_required
def index():
    Cameras = cameras.lst(cameras.query.all())
    if request.cookies.get('menu'):
        menu = request.cookies.get('menu')
    else:
        menu = 'closed'
    cookiejar = {'menu':menu}
    page = '/'
    title = 'Latest Events'
    db.create_all()
    Events = events.query.order_by(desc(events.time)).order_by(desc(events.time)).limit(12).all()
    return cookies.setCookies(cookiejar,make_response(render_template('events.html',Menu=menu,page=page,title=title,events=Events,cameras=Cameras,camera="all")))

@main.route('/latest')
@login_required
def latest():
    return redirect("/")

@main.route('/all')
@login_required
def viewAll():
    Cameras = Cameras = cameras.lst(cameras.query.all())
    if request.cookies.get('menu'):
        menu = request.cookies.get('menu')
    else:
        menu = 'closed'
    cookiejar = {'menu':menu}
    page = '/'
    title = 'Latest Events'
    cookiejar = {'menu':menu}
    page = '/all'
    title = 'All Events'
    db.create_all()
    Events = events.query.order_by(desc(events.time)).order_by(desc(events.time)).all()
    cookiejar = {'menu':'closed'}
    return cookies.setCookies(cookiejar,make_response(render_template('events.html',Menu=menu,page=page,title=title,events=Events,cameras=Cameras,camera="all")))

@main.route('/events/camera/<Camera>')        
@login_required
def viewEventsbyCamera(Camera):
    Cameras = Cameras = cameras.lst(cameras.query.all())
    if request.cookies.get('menu'):
        menu = request.cookies.get('menu')
    else:
        menu = 'closed'
    cookiejar = {'menu':menu}
    if cookies.getCookie('page'):
        page = cookies.getCookie('page')
    else:
        page = "/"
    cookiejar['page'] = page
    cookiejar['cameras'] = str(Cameras)
    title=f"{Camera.title()} Events"
    Events = events.query.filter(events.camera==Camera).order_by(desc(events.time)).all()
    resp = make_response(render_template('events.html',Menu=menu,page=cookiejar['page'],title=title,events=Events,cameras=Cameras,camera=Camera))
    for cookie in cookiejar:
            resp.set_cookie(cookie,cookiejar[cookie])
    return resp

@main.route('/events/camera/<Camera>/<filter>/<value>')
@login_required
def viewEventsbyCameraFiltered(Camera,filter,value):
    cookiejar = {}
    Cameras = Cameras = cameras.lst(cameras.query.all())
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
        page = cookies.getCookie('page')
        cookiejar['page'] = page
        title=f"{Camera.title()} Events by {value.title()}"
        if Camera == "all":
            if filter == 'object':
                Events = events.query.filter(events.object==value).order_by(desc(events.time)).all()
            if filter == 'score':
                Events = events.query.filter(events.score==int(value)).order_by(desc(events.time)).all()
            if filter == 'ack':
                Events = events.query.filter(events.ack==value).order_by(desc(events.time)).all()
        else:
            if filter == 'object':
                Events = events.query.filter(events.camera==Camera,events.object==value).order_by(desc(events.time)).all()
            if filter == 'score':
                Events = events.query.filter(events.camera==Camera,events.score==int(value)).order_by(desc(events.time)).all()
            if filter == 'ack':
                Events = events.query.filter(events.camera==Camera,events.ack==value).order_by(desc(events.time)).all()
    else:
        flashMessage = f"Invalid filter selected. Valid filters are:"
        for fil in validFilters:
            flashMessage += f" {fil}"
        flashMessage+= "."
        flash(flashMessage)
    resp = make_response(render_template('events.html',Menu=menu,page=cookiejar['page'],title=title,events=Events,cameras=Cameras,camera=Camera))
    return cookies.setCookies(cookiejar,resp)

@main.route('/event/<eventid>/<view>')
@login_required
def viewSingle(eventid,view):
    cookiejar = {}
    Cameras = Cameras = cameras.lst(cameras.query.all())
    if request.cookies.get('menu'):
        menu = request.cookies.get('menu')
    else:
        menu = 'closed'
    cookiejar['menu'] = menu
    page = f"/event/{eventid}/{view}"
    cookiejar['page'] = page
    Frigate = api.apiFrigate()
    frigateURL = Frigate['external']
    if view == 'ack':
        api.apiAckEvent(eventid)
    elif view == 'unack':
        api.apiUnackEvent(eventid)
    elif view == 'delOK':
        api.apiDelEvent(eventid)
        resp = redirect(url_for('main.index'))
    query = events.query.filter_by(eventid=eventid).order_by()
    query = events.dict(query)
    for item in query:
        event = query[item]
    if 'event' in locals():
        if event['ack'] == "" and view != 'unack':
            api.apiAckEvent(eventid)
            event['ack'] = "true"
        title = f"<div class='back'><a href='/'><img src='/static/img/back.svg'></a></div><div class='objcam'>{event['object'].title()} in {event['camera'].title()}</div>"
        xx = 0
        for X in ['live','clip','snap']:
            if view == X:
                xx += 1
        if xx > 0:
            if view == 'clip' or view == 'snap':
                title += f"<div class='view20'>Event {view.title()}</div>"
            else:
                title += f"<div class='view20'>{view.title()}</div>"
        else:
            title += "<div class='view20'> </div>"
        resp = make_response(render_template('event.html',Menu=menu,page=page,title=title,event=event,view=view,frigateURL=frigateURL,cameras=Cameras))
    else:
        resp = redirect(url_for('main.index'))
    return cookies.setCookies(cookiejar,resp)

    
