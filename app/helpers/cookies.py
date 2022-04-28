from flask import request, make_response
from app.logit import logit
class cookies:
    def getCookie(cookie):
        if request.cookies.get(cookie):
            return request.cookies.get(cookie)
        else:
            return None
    
    def getMenuCookie():
        if request.cookies.get('menu'):
            return request.cookies.get('menu')
        else:
            return "closed"

    def getCookies(jar):
        cookies = {}
        for cookie in jar:
            if cookie in request.cookies:
                cookies[cookie] = request.cookies.get(cookie)
            else:
                cookies[cookie] = None
        return cookies
        
    def setCookies(jar,resp):
        Response = resp
        for cookie in jar:
            Response.set_cookie(cookie,jar[cookie])
            return Response