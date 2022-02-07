#!/usr/bin/python3
from flask import Flask, render_template, request, Response
#import mysql.connector
import json
import secrets
import binascii
import math
import time
from datetime import datetime, timezone, timedelta

# Google authentication libraries
#from google.oauth2 import id_token as gid_token
#from google.auth.transport import requests as grequests

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config.from_envvar('CONFIG')

# Connect to SQL Database
#db = mysql.connector.connect(
#  user=app.config.get("MYSQL_USER"),
#  password=app.config.get("MYSQL_PASSWORD"),
#  host=app.config.get("MYSQL_ADDR"),
#  database=app.config.get("MYSQL_DB"),
#  use_pure=True)

#googleClientId = app.config.get("GOOGLE_CLIENT_ID")

hostprefix = app.config.get("PERMALINK_PREFIX")

timeshift = app.config.get("TIMEZONE_SHIFT")

class Club:
  def __init__(self, cid, name, sname, ctype, subtype, desc, site,
    banner, sponsor, leader, members, time, campus, room, twitter,
    github, discord, youtube, facebook, instagram, remind, hidden,
    verified
  ):
    self.id = cid
    self.name = name
    self.shortname = sname
    self.type = ctype
    self.subtype = subtype
    self.desc = desc
    self.website = site
    self.banner = banner
    self.sponsor = sponsor
    self.leader = leader
    self.members = members
    self.time = time
    self.campus = campus
    self.room = room

    social = dict()
    social["twitter"] = twitter
    social["github"] = github
    social["discord"] = discord
    social["youtube"] = youtube
    social["facebook"] = facebook
    social["instagram"] = instagram
    social["remind"] = remind
    self.social = social

    self.hidden = hidden
    self.verified = verified

class User:
  def __init__(self, uid, email, name, clubs):
    self.id = uid
    self.emailAddress = email
    self.displayName = name
    self.clubs = clubs

# This function is a safety function that ensures the connection to the
# database server is still alive before trying to use it.
#def sqlSetup():
#    if db.is_connected() != True:
#        db.reconnect(attempts=1, delay=0)

# Checks if the user is logged in
# If they are, then this returns the user
# if not, this returns None
#def checkLoggedIn():
#  token = request.cookies.get("session")
#  if token == None: return None
  
#  sqlSetup()
#  cur = db.cursor(prepared=True)
#  cur.execute("SELECT `Expiration`, `UserID` FROM `sessions` WHERE `Token`=%s LIMIT 1;", (token,))
#  item = cur.fetchone()
#  if item == None:
#    cur.close()
#    db.commit()
#    return None
  
#  exp = item[0]
#  uid = item[1]

#  cur.close()

#  if exp <= time.time():
#    db.commit()
#    return None

#  cur = db.cursor(prepared=True)
#  cur.execute("SELECT `EmailAddress`, `DisplayName`, `Clubs` FROM `users` WHERE `ID`=%s LIMIT 1;", (uid,))

#  item = cur.fetchone()
#  if item == None:
#    cur.close()
#    db.commit()
#    return None

#  u = User(uid, item[0], item[1], json.loads(item[2]))

#  cur.close()
#  db.commit()

#  return u

@app.route("/")
def landing():
  return render_template("home.html")

@app.route("/about")
def route_about():
  return render_template("about.html")

@app.route("/courses")
def route_courses():
  return render_template("courses.html")

@app.route("/explore")
def route_map():
  return render_template("map.html")

@app.route("/clubs")
def route_clubs_list():
  return render_template("clubs.html")

@app.route("/service")
def route_service():
  return render_template("service.html")

@app.route("/help")
def route_help():
  return render_template("help.html")

@app.route("/events")
def route_events():
  return render_template("events.html")

@app.route("/events/json")
def route_events_data():
  events = list()
  #sqlSetup()
  #cur = db.cursor()
  #cur.execute("SELECT `ID`,`Name`,`ClubID`,`StartTime`,`EndTime`,`Description`,`MaxAttendees` FROM `events`;")
  #row = cur.fetchone()
  #while row != None:
  #  # Add item to list of events
  #  item = dict()
  #  item["id"] = row[0]
  #  item["name"] = row[1].decode("utf-8")
  #  item["description"] = row[5].decode("utf-8")
  #  item["club"] = row[2]
  #  item["startTime"] = row[3]
  #  item["endTime"] = row[4]
  #  item["maxAttendees"] = row[6]
  #  events.append(item)

  #  row = cur.fetchone()

  #cur.close()
  #db.commit() # Workaround to prevent an unusual problem

  return Response(json.dumps(events), mimetype="application/json")


#@app.route("/login")
#def route_login():
#  if checkLoggedIn() != None:
#    resp = Response("Already logged in")
#    resp.headers["Location"] = "/management"
#    return resp, 302
#  return render_template("login.html", google_client_id=googleClientId)
'''
@app.route("/login/google", methods=["POST"])
def route_login_google():
  # Process login here
  gtoken = request.form.get("gtk")
  if gtoken == None:
    return "Missing gtk field", 400

  idinfo = gid_token.verify_oauth2_token(gtoken, grequests.Request(), googleClientId)

  if idinfo['hd'] != "allenisd.org" and idinfo['hd'] != "student.allenisd.org":
    return "Only Allen ISD students and staff are authorized to log in", 403

  userid = idinfo['sub']
  email = idinfo['email']
  name = idinfo['name']

  sqlSetup()
  cur = db.cursor(prepared=True)
  cur.execute("SELECT `ID` FROM `users` WHERE `EmailAddress`=%s;", (email,))
  row = cur.fetchone()

  uid = None

  if row == None:
    # account doesn't exist, auto-create one
    cur.close()

    cur = db.cursor(prepared=True)
    cur.execute("INSERT INTO `users` VALUES (null, %s, %s, \"[]\");", (email, name))
    uid = cur.lastrowid
    cur.close()
  else:
    uid = row[0]
    cur.close()

  token = binascii.hexlify(secrets.token_bytes(32)).decode('utf-8')
  exp = math.floor(time.time()) + 3600

  cur = db.cursor(prepared=True)
  cur.execute("INSERT INTO `sessions` VALUES (null, %s, %s, %s);", (token, exp, uid))
  cur.close()

  db.commit()

  resp = Response("Success, sending to landing")
  resp.headers['Location'] = "/management"
  resp.set_cookie('session', token, expires=exp, secure=True, httponly=True)

  return resp, 302

@app.route("/logout")
def route_logout():
  resp = Response("Logged out")
  resp.headers['Location'] = "/"
  resp.set_cookie('session', '', expires=1, secure=True, httponly=True)
  return resp, 302

@app.route("/management")
def route_mgmt_home():
  user = checkLoggedIn()
  if user == None:
    resp = Response("Login is required to view this page")
    resp.headers["Location"] = "/login"
    return resp, 302

  clubs = []
  if len(user.clubs) != 0:
    # The ID values are derived from the database and are assigned by admins,
    # so for the time being it is safe to not use prepared statements.
    query = "SELECT `ID`, `Name` FROM `clubs` WHERE"
    pos = 0
    for i in user.clubs:
      if pos > 0: query = query + " OR"
      query = query + " `ID`=" + str(i)
      pos = pos + 1

    query = query + ";"

    cur = db.cursor()
    cur.execute(query)

    item = cur.fetchone()
    while item != None:
      i = dict()
      i["id"] = item[0]
      i["name"] = item[1].decode("utf-8")
      clubs.append(i)
      item = cur.fetchone()

    cur.close()
    db.commit()
  return render_template("mgmt/home.html", clublist=clubs)

def getClub(cid):
  cur = db.cursor(prepared=True)
  cur.execute("SELECT `Name`,`ShortName`,`Type`,`Subtype`,`Description`,`Website`,"
    + "`BannerImage`,`Sponsor`,`Leader`,`Members`,`MeetingTime`,`LocationCampus`,"
    + "`LocationRoom`,`SocialTwitter`,`SocialGithub`,`SocialDiscord`,`SocialYoutube`,"
    + "`SocialFacebook`,`SocialInstagram`,`Remind`,`Hidden`,`Verified`"
    + " FROM `clubs` WHERE `ID`=%s LIMIT 1;", (cid,)
  )

  i = cur.fetchone()
  if i == None:
    cur.close()
    db.commit()
    return None

  c = Club(
    cid,
    i[0],
    i[1],
    i[2],
    i[3],
    i[4],
    i[5],
    i[6],
    i[7],
    i[8],
    i[9],
    i[10],
    i[11],
    i[12],
    i[13],
    i[14],
    i[15],
    i[16],
    i[17],
    i[18],
    i[19],
    (i[20] == 1),
    (i[21] == 1)
  )

  cur.close()
  db.commit()

  return c

@app.route("/management/club/<cid>")
def route_mgmt_club_landing(cid):
  cid = int(cid)
  
  user = checkLoggedIn()
  if user == None:
    resp = Response("Login is required to view this page")
    resp.headers["Location"] = "/login"
    return resp, 302

  if cid not in user.clubs:
    resp = Response("User is not authorized to access this club")
    resp.headers["Location"] = "/management"
    return resp, 302

  club = getClub(cid)
  if club == None:
    resp = Response("Club does not exist")
    resp.headers["Location"] = "/management"
    return resp, 302

  return render_template("mgmt/club-landing.html", club=club)

@app.route("/management/club/<cid>/new-event", methods=['GET','POST'])
def route_mgmt_club_create_event(cid):
  cid = int(cid)
  
  user = checkLoggedIn()
  if user == None:
    resp = Response("Login is required to view this page")
    resp.headers["Location"] = "/login"
    return resp, 302

  if cid not in user.clubs:
    resp = Response("User is not authorized to access this club")
    resp.headers["Location"] = "/management"
    return resp, 302

  club = getClub(cid)
  if club == None:
    resp = Response("Club does not exist")
    resp.headers["Location"] = "/management"
    return resp, 302

  if request.method == "POST":
    # process update
    signInCode = binascii.hexlify(secrets.token_bytes(8)).decode('utf-8')

    name = request.form.get("title")
    day = request.form.get("day")
    stime = request.form.get("stime")
    etime = request.form.get("etime")
    desc = request.form.get("desc")
    attendees = request.form.get("attendees")
    
    # This is probably prone to several different kinds of errors, someone
    # should improve it
    sdt = datetime.strptime(day + " " + stime, "%Y-%m-%d %H:%M")
    st = sdt.replace(tzinfo=timezone(timedelta(hours=timeshift))).timestamp()

    edt = datetime.strptime(day + " " + etime, "%Y-%m-%d %H:%M")
    et = edt.replace(tzinfo=timezone(timedelta(hours=timeshift))).timestamp()

    cur = db.cursor(prepared=True)
    cur.execute("INSERT INTO `events` VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);", (
      name, club.id, st, et, desc, attendees, signInCode
    ))

    cur.close()
    db.commit()

    return render_template("mgmt/event-create-success.html", code=signInCode, host=hostprefix, club=club)
  else:
    return render_template("mgmt/event-create.html", club=club)

'''
if __name__ == "__main__":
  app.run(debug=True)

