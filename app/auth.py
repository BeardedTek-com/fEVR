import ipaddress
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from IPy import IP

from .models.models import User, apiAuth, cameras
from . import db
from .rndpwd import randpwd
from  .helpers.cookies import cookies

auth = Blueprint('auth', __name__)

@auth.route('/auth/add/key/<name>/<ip>/<limit>')
@login_required
def apiAuthKeyAdd(name,ip,limit):
    def validIP(ip):
        try:
            IP(ip)
            return True
        except:
            return False
    if current_user.group == "admin":
        if validIP(ip):
            db.create_all()
            key = randpwd.generate(key=True)
            auth = apiAuth(name=name,authIP=ip,key=key,limit=int(limit))
            db.session.add(auth)
            db.session.commit()
            value = {"Authorized":True,"name":name,"ip":ip,"limit":limit,"key":key,"expired":False}
        else:
            value = {"Authorized":False,"Reason":"Invalid IP"}
    else:
        value = {"Authorized":False,"Reason":"Admin Only"}
    return jsonify(value)

@auth.route('/auth/add/key',methods=['POST'])
@login_required
def apiAuthKeyAddPost():
    def validIP(ip):
        try:
            IP(ip)
            return True
        except:
            return False
    ip = request.form.get('ip')
    name = request.form.get('name')
    limit = request.form.get('limit')
    if current_user.group == "admin":
        if validIP(ip):
            db.create_all()
            key = randpwd.generate(key=True)
            auth = apiAuth(name=name,authIP=ip,key=key,limit=int(limit))
            db.session.add(auth)
            db.session.commit()
            value = {"Authorized":True,"name":name,"ip":ip,"limit":limit,"key":key,"expired":False}
        else:
            value = {"Authorized":False,"Reason":"Invalid IP"}
    else:
        value = {"Authorized":False,"Reason":"Admin Only"}
    return jsonify(value)

@auth.route('/apiAuth',methods=['POST'])
def apiAuthenticate():
    ip = request.remote_addr
    auth = {"auth":False,"name":None,"authIP":ip,"changed":False,"remember":False}
    requestData = request.get_json()
    key = None
    if 'key' in requestData:
        key = requestData['key']
        entries = apiAuth.query.all()
        if entries:
            for entry in entries:
                if entry.key == key:
                    # Check if all of the following match:
                    #   - ip address
                    #   - key
                    #   - key expiry
                    if entry.key==key and not entry.expired:
                        auth['auth'] = True
                        auth['name'] = entry.name
                        auth['authIP'] = ip
                        login_user(entry,remember=True)
                        # Check the key limits
                        # Keys can be use limited.
                        # A user that has just a limited key can only log into the site X number of times before key expires
                        if entry.limit != 0:
                            if entry.limit > 1:
                                entry.limit -= 1
                                auth['changed'] = True
                            # If this is the key's last use, make sure to expire it.
                            elif entry.limit == 1:
                                entry.limit = 0
                                entry.expired = True
                                auth['changed'] = True
                        # If we changed they key limit or set it to expired, commit it to the database.
                        if auth['changed']:
                            db.session.commit()
    return jsonify(auth)

@auth.route('/login',methods=['GET'])
def login():
    Cookies = cookies.getCookies(['menu'])
    fwd = "/"
    fwdName = "access fEVR"
    fwd = request.args.get('next')
    if fwd != None:
        fwd.replace('%2F','/')
        values = {"/": "access fEVR", "/event":"view this event","/events":"view events"}
        for val in values:
            if fwd == val:
                fwdName = values[val]
    else:
        fwd = "/"
    return render_template('login.html',menu=Cookies['menu'],fwd=fwd,fwdName=fwdName)
    
@auth.route('/login', methods=['POST'])
def loginProcessForm():
    
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    fwd = request.form.get('fwd')

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(fwd)

@auth.route('/signup')
def signup():
    Cookies = cookies.getCookies(['menu','page'])
    cookiejar = {'page':'/'}
    db.create_all()
    if User.query.first() == None:
        resp = make_response(render_template('setupadmin.html',type='admin'))
    else:
        resp = make_response(render_template('signup.html',menu=Cookies['menu'],page=Cookies['page']))
    return cookies.setCookies(cookiejar,resp)

@auth.route('/signup', methods=['POST'])
def signupProcessForm():
    status = {'db':{'cameras':False,'frigate':False,'User':False,'apiAuth':False,'config':False}}
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address exists.  Did you forget your password?')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256', items=status))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout',methods=['GET'])
@login_required
def logout():
    fwd = "/"
    fwd = request.args.get('page')
    if fwd == None:
        fwd = "/"
    fwd.replace('%2F','/')
    logout_user()
    cookiejar = {'menu':'closed'}
    return cookies.setCookies(cookiejar,make_response(redirect(fwd)))

@auth.route('/profile')
@login_required
def profile():
    Cameras = Cameras = cameras.lst(cameras.query.all())
    Cookies = cookies.getCookies(['menu','page'])
    cookiejar = {'page':'/profile'}
    user = current_user
    keys = apiAuth.query.all()
    return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=Cookies['menu'],cameras=Cameras,user=user,keys=keys,page=Cookies['page'])))

@auth.route('/profile',methods=['POST'])
@login_required
def profilePost():
    user = current_user.name
    Cookies = cookies.getCookies(['menu','page'])
    page = "/profile"
    menu=Cookies['menu']
    cookiejar = {'page':page}
    keys = apiAuth.query.all()
    form = {}
    Password = 0
    retypePassword = 0
    missingFields =[]
    for value in ['email','name','group','password','retypePassword']:
        if request.form.get(value):
            form[value] = request.form.get(value)
        else:
            if value == 'password':
                Password = 1
            elif value == 'retypePassword':
                retypePassword = 1
            else:
                missingFields.append(value)
        if missingFields:
            flashmsg = "Required fields missing: "
            for field in missingFields:
                flashmsg += f"{field} "
            flash(flashmsg)
            return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))
    query = User.query.filter_by(email=form['email']).first()
    if query.email == form['email']:
        query.name = form['name']
        changePassword = Password + retypePassword
        if changePassword == 0:
            print(changePassword)
            if form['password'] == form['retypePassword']:
                password = generate_password_hash(form['password'], method='sha256')
                if query.password != password:
                    query.password = password
                    flash('Password successfully changed.')
                    return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))
                else:
                    flash('Please use a different password.')
                    return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))
            else:
                flash('Passwords do not match.  Try again.')
                return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))
        elif changePassword == 1:
            if Password == 1:
                flash('You must type your password')
                return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))
            elif retypePassword == 1:
                flash('You must retype your password')
                return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))
        db.session.commit()
        return cookies.setCookies(cookiejar,make_response(render_template('user.html',menu=menu,user=user,keys=keys,page=page)))