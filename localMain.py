#!/usr/bin/python3
from flask import Flask, render_template, request, Response, jsonify, abort, request_started, session, redirect
import awsController
import json
import secrets
import binascii
import math
import time
import os
from datetime import datetime, timezone, timedelta
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import requests
import cachecontrol
import pathlib

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.secret_key = "verySecretiveP@ss2412!!"

#just for now
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

googleClientId = "70595814458-s2br8ao60ukkg8evl908okg6qtk786ei.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "STEAMLifeFlaskClientKeys.json")
flow = Flow.from_client_secrets_file(
  client_secrets_file=client_secrets_file,
  scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
  redirect_uri="http://127.0.0.1:5000/callback")

#app.config.from_envvar('CONFIG')

#timeshift = app.config.get("TIMEZONE_SHIFT")

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

#make sure user is logged in for certain pages
def dashboard_login_is_required(function):
  def wrapper(*args, **kwargs):
    if "google_id" not in session:
      return abort(403) # forbidden
    else:
      return function()
  return wrapper
def management_login_is_required(function):
  def wrapperm(*args, **kwargs):
    if "google_id" not in session:
      return abort(403) # forbidden
    else:
      return function()
  return wrapperm
def map_login_is_required(function):
  def wrappers(*args, **kwargs):
    if "google_id" not in session:
      return abort(403) # forbidden
    else:
      return function()
  return wrappers

def get_user_email():
  userEmail = ""
  try: 
    userEmail = session["email"]
  except:
    print("Could not get email")
  return userEmail
  
def get_user_name():
  userName = ""
  try: 
    userName = session["name"]
  except:
    print("Could not get email")
  return userName

@app.route("/")
def landing():
  return render_template("home.html", email=get_user_email())

@app.route("/about")
def route_about():
  return render_template("about.html", email=get_user_email())

@app.route("/courses")
def route_courses():
  return render_template("courses.html", email=get_user_email())

@app.route("/explore")
@map_login_is_required
def route_map():
  return render_template("map.html", email=get_user_email())

@app.route("/comm/json")
def route_comm_data():
  return jsonify(Items=awsController.get_comm_items())

@app.route("/clubs", methods=['POST', 'GET'])
def route_clubs_list():
  if (request.method == "POST"):
    clubAddData = request.get_json()
    if (clubAddData["email"] == session["email"]):
      awsController.add_club(session["email"], session["name"], clubAddData["clubID"])
  return render_template("clubs.html", email=get_user_email())

@app.route("/clubs/json")
def route_clubs_data():
  return jsonify(Items=awsController.get_club_items())

@app.route("/service", methods=['POST', 'GET'])
def route_service():
  if (request.method == "POST"):
    serviceAddData = request.get_json()
    if (serviceAddData["email"] == session["email"]):
      awsController.add_user_service(session["email"], session["name"], serviceAddData["serviceID"])
  return render_template("service.html", email=get_user_email())

@app.route("/service/json")
def route_service_data():
  return jsonify(Items=awsController.get_service_items())

@app.route("/help")
def route_help():
  return render_template("help.html", email=get_user_email())

@app.route("/events")
def route_events():
  return render_template("events.html", email=get_user_email())

@app.route("/events/json")
def route_events_data():
  return jsonify(Items=awsController.get_calendar_items())

@app.route("/gallery")
def route_gallery():
  return render_template("gallery.html", email=get_user_email())

@app.route("/archive")
def route_archive():
  return render_template("archive.html", email=get_user_email())

@app.route("/callback")
def route_callback():
  flow.fetch_token(authorization_response=request.url)
  if not session["state"] == request.args["state"]:
    redirect("/login")
  credentials = flow.credentials
  request_session = requests.session()
  cached_session = cachecontrol.CacheControl(request_session)
  token_request = google.auth.transport.requests.Request(session=cached_session)

  id_info = id_token.verify_oauth2_token(
    id_token=credentials.id_token,
    request=token_request,
    audience=googleClientId
  )
  session["google_id"] = id_info.get("sub")
  session["email"] = id_info.get("email")
  session["name"] = id_info.get("name")
  awsController.check_user(session["email"])
  oldName = awsController.find_user_name(session["email"])
  #awsController.rename_user(oldName, session["name"], session["email"])
  return redirect("/dashboard")

@app.route("/login")
def route_login():
  try:
    if (session["email"]):
      return redirect("/dashboard")
  except:
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/user/json")
def route_user_data():
  return jsonify(Items=awsController.get_user_items())

@app.route("/dashboard")
@dashboard_login_is_required
def route_dashboard():
  return render_template("dashboard.html", email=get_user_email(), name=get_user_name())

@app.errorhandler(401)
def access_denied(error):
  return render_template('401.html', title='401', email=get_user_email()), 401

@app.errorhandler(403)
def page_forbidden(error):
  return render_template('403.html', title='403', email=get_user_email()), 403

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html', title='404', email=get_user_email()), 404

@app.route("/unauthorized")
def route_unauthorized():
  return abort(401)

@app.route("/forbidden")
def route_forbidden():
  return abort(403)

@app.route("/page-not-found")
def route_page_not_found():
  return abort(404)

@app.route("/management", methods=['POST', 'GET'])
@management_login_is_required
def route_management():
  if (request.method == "POST"):
    editData = request.get_json()
    try:
      editInfo = editData["Club"]
      editMembers = editData["Member"]
      awsController.edit_club_info(editInfo["Club-Name"], editInfo["ID"], editInfo["Description"], editInfo["Leaders"], editInfo["Location"], editInfo["Meeting"], editInfo["Social"], editInfo["Sponsors"], editInfo["Subtype"], editInfo["Type"], editInfo["Website"], editInfo["Add-Owners"], editInfo["Remove-Owners"])
      awsController.edit_club_member(editMembers["Members-Add"], editMembers["Members-Remove"], editInfo["ID"])
    except:
      print("not club data")
    try:
      editEvents = editData["Events"]
      awsController.edit_club_event(editEvents)
    except:
      print("not event data")
    try:
      editServices = editData["Services"]
      awsController.edit_club_service(editServices)
    except:
      print("not service data")
  return render_template("management.html", email=get_user_email())

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)

