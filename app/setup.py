from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models.models import User,frigate,cameras,events,apiAuth,config,mqtt
from sqlalchemy import desc, exc
from .helpers.drawSVG import drawSVG
from . import db
from .rndpwd import randpwd
from .helpers.cookies import cookies
from os.path import exists
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
    status = {'db':{'cameras':False,'frigate':False,'mqtt':False,'other':False}}
    tables = {
        'frigate':frigate,
        'cameras':cameras,
        'mqtt':apiAuth,
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
            next="/setup/mqtt"
            template = "setupfrigate.html"
            resp = render_template(template,frigate=frigate.query.all(),cameras=Cameras,menu=menu,next=next,label=label,page=page,items=status,Item=Item,user=user)
        elif Item == 'mqtt':
            label = 'MQTT Client Setup'
            next = '/setup/config'
            template = "setupmqtt.html"            
            MQTT = mqtt.query.first()
            command = f"BROKER   : {MQTT.broker}<br/> \
                        PORT     : {MQTT.port}<br/> \
                        MQTT USER: {MQTT.user}<br/> \
                        MQTT PASS: {MQTT.password}<br/> \
                        TOPIC    : {MQTT.topics}<br/> \
                        FEVR     : {MQTT.fevr}<br/> \
                        PROTOCOL : {MQTT.https}<br/> \
                        API KEY  : {MQTT.key}<br/>"
            resp = render_template(template,cameras=Cameras,menu=menu,next=next,label=label,page=page,items=status,Item=Item,user=user,command=command)
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
def apiAddCameraPost():
    if current_user.group == "admin":
        db.create_all()
        camera = request.form.get('camera')
        hls = request.form.get('hls')
        rtsp = request.form.get('rtsp')
        if request.form.get('show') == "true":
            show = True
        else:
            show = False
        camera = cameras(camera=camera,hls=hls,rtsp=rtsp,show=show)
        db.session.add(camera)
        db.session.commit()
        resp = redirect('/setup/cameras')
    else:
        resp = redirect('/')
    return resp

@setup.route('/setup/cameras/edit/<camera>',methods=['POST'])
@login_required
def apiEditCameraPost(camera):
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
            if request.form.get('show') != "true":
                camEdit.show = False
                edit = True
        else:
            if request.form.get('show') == "true":
                camEdit.show = True
                edit = True
        if edit:
            db.session.commit()
    resp = redirect('/setup/cameras')
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
        frigateEdit = frigate.query.filter_by(Frigate=Frigate).first()
        if frigateEdit.name != request.form.get('url'):
            frigateEdit.name = request.form.get('url')
            edit = True
        if edit:
            db.session.commit()
    resp = redirect('/setup/frigate')
    return resp

@setup.route('/setup/mqtt/add',methods=['POST'])
@login_required
def setupAddMqttPost():
    if current_user.group == "admin":
        db.create_all()
        broker = request.form.get('broker')
        port = request.form.get('port')
        brokerU = request.form.get('brokerU')
        if not brokerU:
            brokerU == "\"\""
        brokerP = request.form.get('brokerP')
        if not brokerP:
            brokerP == "\"\""
        topics = request.form.get('topics')
        https = request.form.get('https')
        fevr = request.form.get('fevr')
        fevrport = request.form.get('fevrport')
        key = request.form.get('key')
        user = ""
        password = ""
        fields = {"broker":broker,"port":port,"user":brokerU,"password":brokerP,"topics":topics,"https":https,"fevr":fevr,"fevrport":fevrport,"key":key}
        Valid = True
        for field in fields:
            if not fields[field] and field == "broker" and field == "key":
                flash(f"{field.title()} is a required field.")
                Valid = False
            else:
                if field == "https":
                    if fields[field] != "http" and fields[field] != "https":
                        flash(f"https field must be either http or https")
                        flash(f"defaulting to 'http://'")
                        https="http://"
                elif field == "key":
                    if 128 > len(fields[field]) > 128:
                        flash(f"key must be exactly 128 characters long.")
                        Valid = False
                elif field == "port":
                    try:
                        port = int(port)
                    except:
                        flash("Port must be an integer.  If unsure, just enter 1883.")
                        Valid = False
                elif field == "user":
                    if not fields[field]:
                        user=""
                    else:
                        user = brokerU
                elif field == "password":
                    if not fields[field]:
                        password=""
                    else:
                        password = brokerP
                elif field == "fevrport":
                    if https == "https://":
                        if fevrport != "443":
                            fevr = f"{fevr}:{fevrport}"
                    elif https == "http":
                        if fevrport != "80":
                            fevr = f"{fevr}:{fevrport}"
                    else:
                        fevr = f"{fevr}:{fevrport}"
                        
        if Valid:
            if not user:
                user = ""
            if not password:
                password = ""
            mqtt.query.all().delete()
            MQTT = mqtt(port=port,topics=topics,user=user,password=password,https=https,fevr=fevr,broker=broker,key=key)
            db.session.add(MQTT)
            db.session.commit()
            MQTT= mqtt.query.first()
            command = f"/fevr/venv/bin/python /fevr/app/mqtt_client"
            if MQTT.port != 1883:
                command += f" -p {MQTT.port}"
            if MQTT.topics != "frigate/+":
                command += f" -t {MQTT.topics}"
            if MQTT.user != "" and MQTT.password != "":
                command += f" -u {MQTT.user} -P {MQTT.password}"
            if MQTT.https == "https":
                command += " -s "
            if MQTT.fevr != "localhost:5090":
                command += f" -f {MQTT.fevr}"
            command += f" {MQTT.broker} {MQTT.key}"
            # Write new run_mqtt_client.sh:
            with open('run_mqtt_client.sh', "w") as myfile:
                myfile.write(f"#!/bin/sh\n{command}")
        resp = redirect('/setup/mqtt')
        return resp
