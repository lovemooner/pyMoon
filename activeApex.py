import requests

apex_login_url= "https://apex.oracle.com/pls/apex/f?p=4550:1"

# change pwd page https://apex.oracle.com/pls/apex/f?p=4350:68:100612242942094::::P68_USER_ID,P68_ASK_CURRENT:18092641423800972273,Y&cs=3EzYgWMRWzGlKl8Sv2bY9W4NxBhfvm0Cv3erR_QuddeAkAaQsnI6Sjinri86BF9nV1hcy_Ak_hJE7u03o5TFdWQ

def dologin():
    resp = requests.get(apex_login_url)
    vals = resp.url.split("=")[1].split(":")
    app, page, apex_session = (vals[0], vals[1], vals[2])
    url = "https://apex.oraclecorp.com/pls/apex/f?p=%s:%s:%s:::::" % (app, page, apex_session)
    print(url)

dologin()