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

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import exc

from app.models.user import User
from app.models.frigate import frigate
from app.models.cameras import cameras
from app.models.config import config

from app import db
from app.helpers.rndpwd import randpwd
from app.helpers.cookies import cookies
from app.helpers.logit import logit


setup = Blueprint('setup', __name__)

@setup.route('/setup')
def setupFwd():
    return redirect("/setup/admin")

@setup.route('/setup/admin')
def setupAdmin():
    # First, let's create the database
    db.create_all()
    admin = User.query.filter_by(group='admin').first()
    if admin:
        adname = admin.name
        admail = admin.email
        admin = [adname,admail]
        resp = redirect('/setup/cameras')
    else:
        # First, let's create the database
        db.create_all()
        status = {'db':{'cameras':False,'frigate':False,'User':False,'apiAuth':False,'config':False}}
        # Sanity checks...
        admin = User.query.filter_by(group='admin').first()
        resp = render_template('setupadmin.html',passwd = randpwd.generate(),items=status,next="cameras")
    return resp

@setup.route('/setup/<Item>')
@login_required
def setupfEVR(Item):
    user = current_user
    Cameras =[]
    for row in cameras.query.all():
        Cameras.append(row.camera)
    menu=cookies.getCookie('menu')
    status = {'db':{'cameras':False,'frigate':False,'other':False}}
    tables = {
        'frigate':frigate,
        'cameras':cameras,
        'other':config
    }
    for table in tables:
        try:
            tables[table].query.first()
            status['db'][table] = True
        except exc.OperationalError:
            status['db'][table] = False
    if Item == status:
        return status
    else:
        page=f"/setup/{Item}"
        label = f"{Item.title()} Setup"
        if Item == 'start' or Item == 'fevr' or Item == 'admin':
            next='frigate'
            label = 'fEVR Setup'
        elif Item == 'cameras':
            next="/setup/frigate"
            template = "setupcameras.html"
            resp = render_template(template,Cameras=cameras.query.all(),cameras=Cameras,menu=menu,next=next,label=label,page=page,items=status,Item=Item,user=user)
        elif Item == 'frigate':
            next="/setup/other"
            template = "setupfrigate.html"
            resp = render_template(template,frigate=frigate.query.all(),cameras=Cameras,menu=menu,next=next,label=label,page=page,items=status,Item=Item,user=user)
        elif Item == 'config' or Item == 'other':
            label = "Other"
            next = '/'
            template = "setupconfig.html"
            resp = render_template(template,frigate=frigate.query.all(),cameras=Cameras,menu=menu,next=next,label=label,page=page,items=status,Item=Item,user=user)
        else:
            label = "Cameras"
            next="/setup/frigate"
            template = "setupcameras.html"
            flash(f"{Item} not a valid setup paramater.  Back to the start you go.")
            resp = render_template(template,Cameras=cameras.query.all(),cameras=Cameras,menu=menu,next=next,label=label,page=page,items=status,Item=Item,user=user)
        return resp

@setup.route('/setup/admin', methods=['POST'])
def setupAdminProcessForm():
    # Sanity checks...
    admin = User.query.filter_by(group='admin').first()
    if admin: # If an admin already exists, then go to signup page instead.
        flash('There can be only one!')
        return redirect(url_for('auth.signup'))
    else:
        # code to validate and add user to database goes here
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        retypePassword = request.form.get('retypePassword')

        if password != retypePassword: # Do passwords match?
            flash('Passwords do not match.')
            return redirect(url_for('setup.setupAdmin'))
        
        emailCheck = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if emailCheck: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email Already Exists.')
            return redirect(url_for('setup.setupAdmin'))
        
        nameCheck = User.query.filter_by(name=name).first()
        if nameCheck: # Does this username already exist?
            flash('Username Taken')
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), group='admin', enabled=True, resetpwd=False)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login?next=%2Fsetup%2Fcameras")

@setup.route('/setup/cameras/add',methods=['POST'])
@login_required
def setupAddCameraPost():
    if current_user.group == "admin":
        db.create_all()
        camera = request.form.get('camera')
        hls = request.form.get('hls')
        rtsp = request.form.get('rtsp')
        show = True if request.form.get('show') else False
        logit.execute(f"Show: {show}",src="SETUP | Camera")
        camera = cameras(camera=camera,hls=hls,rtsp=rtsp,show=show)
        try:
            db.session.add(camera)
            db.session.commit()
            resp = redirect('/setup/cameras')
        except Exception as e:
            flash(e)
            resp = redirect('/setup/cameras')
    else:
        resp = redirect('/')
    return resp

@setup.route('/setup/cameras/edit/<camera>',methods=['POST'])
@login_required
def setupEditCameraPost(camera):
    if current_user.group == "admin":
        edit = False
        camEdit = cameras.query.filter_by(camera=camera).first()
        if camEdit.hls != request.form.get('hls'):
            camEdit.hls = request.form.get('hls')
            edit = True
        if camEdit.rtsp != request.form.get('rtsp'):
            camEdit.rtsp = request.form.get('rtsp')
            edit = True
        if camEdit.show:
            if not request.form.get('show'):
                camEdit.show = False
                edit = True
        else:
            if request.form.get('show'):
                camEdit.show = True
                edit = True
        if edit:
            db.session.commit()
        resp = redirect('/setup/cameras')
    else:
        resp = redirect('/')
    return resp


@setup.route('/setup/cameras/del/<Camera>',methods=['POST'])
@login_required
def setupDelCameraPost(Camera):
    Cameras = cameras.query.all()
    cookiejar = {}
    cookiejar['menu'] = cookies.getCookie('menu') if cookies.getCookie('menu') else "closed"
    cookiejar['page'] = cookies.getCookie('page') if cookies.getCookie('page') else "/"
    cookiejar['cameras'] = str(Cameras)
    if current_user.group == "admin":
        cameras.query.filter_by(name=Camera).delete()
        db.session.commit()
        resp = redirect('/setup/cameras')
    else:
        resp = redirect('/')
    return resp
        
@setup.route('/setup/frigate/add',methods=['POST'])
@login_required
def setupAddFrigatePost():
    if current_user.group == "admin":
        db.create_all()
        name = request.form.get('name')
        url = request.form.get('url')
        
        Frigate = frigate(name=name,url=url)
        db.session.add(Frigate)
        db.session.commit()
        flash(f"{name} / {url} successfully added.")
        resp = redirect('/setup/frigate')
    else:
        resp = redirect('/')
    return resp

@setup.route('/setup/frigate/edit/<Frigate>',methods=['POST'])
@login_required
def setupEditFrigatePost(Frigate):
    if current_user.group == "admin":
        edit = False
        frigateEdit = frigate.query.filter_by(name=Frigate).first()
        if frigateEdit.name != request.form.get('name'):
            frigateEdit.name = request.form.get('name')
            edit = True
        if frigateEdit.url != request.form.get('url'):
            frigateEdit.url = request.form.get('url')
            edit = True
        if edit:
            db.session.commit()
        resp = redirect('/setup/frigate')
    else:
        resp = redirect('/')
    return resp

@setup.route('/setup/frigate/del/<Frigate>',methods=['POST'])
@login_required
def setupDelFrigatePost(Frigate):
    Cameras = cameras.query.all()
    cookiejar = {}
    cookiejar['menu'] = cookies.getCookie('menu') if cookies.getCookie('menu') else "closed"
    cookiejar['page'] = cookies.getCookie('page') if cookies.getCookie('page') else "/"
    cookiejar['cameras'] = str(Cameras)
    if current_user.group == "admin":
        frigate.query.filter_by(name=Frigate).delete()
        db.session.commit()
        resp = redirect('/setup/cameras')
    else:
        resp = redirect('/')
    return resp