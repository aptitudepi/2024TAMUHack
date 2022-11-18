#!/usr/bin/python3
from types import TracebackType
from flask import Flask, render_template, request, Response, jsonify, abort, request_started, session, redirect, url_for
#from flask_session import Session
import awsController
import json
import secrets
import binascii
import math
import time
import os
from datetime import datetime, timezone, timedelta
from oauthlib.oauth2 import WebApplicationClient
import requests
import cachecontrol
import pathlib
import string
import pytz

#Note - this is the main.py file that I am using as of 9/26/22



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

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def get_user_email():
  userEmail = "Other-User"
  try: 
    userEmail = session["email"]
  except:
    print("Could not get email")
  print(userEmail)
  return userEmail
def get_user_name():
  userName = ""
  try: 
    userName = session["name"]
  except:
    print("Could not get email")
  return userName
def get_other_user_name():
  userName = ""
  try: 
    userNameArr = session["email"].split("@")[0].split(".")
    for partName in userNameArr:
      userName += partName
      if (userNameArr.index(partName)+1 != len(userNameArr)):
        userName += " "
    userName = string.capwords(userName)
  except:
    print("Could not get email")
  return userName
def get_users_data():
  return json.dumps({"Items" : awsController.get_user_items()})
def next_log_id():
  return (awsController.last_log_id()) + 1
def get_now():
  central = pytz.timezone('US/Central')
  return datetime.now(central).strftime("%d/%m/%Y %H:%M:%S")

@app.route("/")
def landing():
  return render_template("home.html", email=get_user_email())

@app.route("/about")
def route_about():
  return render_template("about.html", email=get_user_email())

@app.route("/courses")
def route_courses():
  return render_template("courses.html", email=get_user_email())

@app.route("/day/json")
def route_day_data():
  return jsonify(Items=awsController.get_day_items())

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
      awsController.add_club(session["email"], get_other_user_name(), clubAddData["clubID"])
  return render_template("clubs.html", email=get_user_email(), userData=get_users_data())

@app.route("/clubs/json")
def route_clubs_data():
  return jsonify(Items=awsController.get_club_items())

@app.route("/service", methods=['POST', 'GET'])
def route_service():
  if (request.method == "POST"):
    serviceAddData = request.get_json()
    if (serviceAddData["email"] == session["email"]):
      awsController.add_user_service(session["email"], get_other_user_name(), serviceAddData["serviceID"])
  return render_template("service.html", email=get_user_email(), userData=get_users_data())

@app.route("/service/json")
def route_service_data():
  return jsonify(Items=awsController.get_service_items())

@app.route("/help")
def route_help():
  return render_template("help.html", email=get_user_email())

@app.route("/events")
def route_events():
  return render_template("events.html", email=get_user_email(), userData=get_users_data())

@app.route("/events/json")
def route_events_data():
  return jsonify(Items=awsController.get_calendar_items())

@app.route("/gallery")
def route_gallery():
  return render_template("gallery.html", email=get_user_email())

@app.route("/privacy-policy")
def route_privacy():
  return render_template("privacy.html")

@app.route("/terms")
def route_terms():
  return render_template("terms.html")

@app.route("/archive")
def route_archive():
  return render_template("archive.html", email=get_user_email())

@app.route("/callback")
def route_callback():
  try:
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
      token_endpoint,
      authorization_response=request.url,
      redirect_url=request.base_url,
      code=code
    )
    token_response = requests.post(
      token_url,
      headers=headers,
      data=body,
      auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
      session["google_id"] = userinfo_response.json()["sub"]
      session["email"] = userinfo_response.json()["email"]
      session["name"] = userinfo_response.json()["name"]
    awsController.check_user(session["email"], session["name"])
    oldName = awsController.find_user_name(session["email"])
    logDetails = ""
    logTime = ""
    try:
      logTime = get_now()
    except:
      print("could not get time")
    try:
      logDetails = "Signing in user: "
      logDetails += session["email"]
    except:
      print("error occurred when logging")
    awsController.add_log(next_log_id(), get_user_email(), "Sign-In", logTime, logDetails)
  except:
    print("a callback error occurred")
  return redirect("/dashboard")

@app.route("/login")
def route_login():
  try:
      if (session["email"]):
        return redirect("/dashboard")
  except:
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/user/json", methods=['POST', 'GET'])
def route_user_data():
  try:
    getUserData = request.args.get('userAuthorized')
    if (getUserData == "true"):
      logDetails = ""
      logTime = ""
      try:
        logTime = get_now()
      except:
        print("could not get time")
      try:
        logDetails = "Accessing secret user data, user: "
        logDetails += session["email"]
      except:
        print("error occurred when logging")
      #awsController.add_log(28, "lkjsfd", "Data-Warning", "asdf", "asf")
      awsController.add_log(next_log_id(), get_user_email(), "Data-Warning", logTime, logDetails)
      return jsonify(Items=awsController.get_user_items())
  except:
    return jsonify(Items=[])
  return jsonify(Items=[])

@app.route("/dashboard")
@dashboard_login_is_required
def route_dashboard():
  return render_template("dashboard.html", email=get_user_email(), name=get_user_name(), userData=get_users_data())

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
      logDetails = ""
      logTime = ""
      try:
        logTime = get_now()
      except:
        print("could not get time")
      try:
        logDetails = "Editing club page, user: "
        logDetails += session["email"]
        logDetails += ", edited data: "
        logDetails += json.dumps(editInfo)
      except:
        print("error occurred when logging")
      awsController.add_log(next_log_id(), get_user_email(), "Edit-Page", logTime, logDetails)
      logDetails = ""
      logTime = ""
      try:
        logTime = get_now()
      except:
        print("could not get time")
      try:
        logDetails = "Possibly editing club members, user: "
        logDetails += session["email"]
        logDetails += ", edited data: "
        logDetails += json.dumps(editMembers)
      except:
        print("error occurred when logging")
      awsController.add_log(next_log_id(), get_user_email(), "Edit-Members", logTime, logDetails)
    except:
      print("not club data")
    try:
      editEvents = editData["Events"]
      awsController.edit_club_event(editEvents)
      logDetails = ""
      logTime = ""
      try:
        logTime = get_now()
      except:
        print("could not get time")
      try:
        logDetails = "Editing or adding club event, user: "
        logDetails += session["email"]
        logDetails += ", edited data: "
        logDetails += json.dumps(editEvents)
      except:
        print("error occurred when logging")
      awsController.add_log(next_log_id(), get_user_email(), "Edit-Event", logTime, logDetails)
    except:
      print("not event data")
    try:
      editServices = editData["Services"]
      awsController.edit_club_service(editServices)
      logDetails = ""
      logTime = ""
      try:
        logTime = get_now()
      except:
        print("could not get time")
      try:
        logDetails = "Editing or adding club service, user: "
        logDetails += session["email"]
        logDetails += ", edited data: "
        logDetails += json.dumps(editServices)
      except:
        print("error occurred when logging")
      awsController.add_log(next_log_id(), get_user_email(), "Edit-Service", logTime, logDetails)
    except:
      print("not service data")
    try:
      editComms = editData["Communication"]
      awsController.edit_club_communication(editComms)
      logDetails = ""
      logTime = ""
      try:
        logTime = get_now()
      except:
        print("could not get time")
      try:
        logDetails = "Sending or editing club message, user: "
        logDetails += session["email"]
        logDetails += ", edited data: "
        logDetails += json.dumps(editComms)
      except:
        print("error occurred when logging")
      awsController.add_log(next_log_id(), get_user_email(), "Send-Message", logTime, logDetails)
    except:
      print("not service data")
  return render_template("management.html", email=get_user_email(), userData=get_users_data())

@app.route("/logout")
def logout():
  logDetails = ""
  logTime = ""
  try:
    logTime = get_now()
  except:
    print("could not get time")
  try:
    logDetails = "Signing out user: "
    logDetails += session["email"]
  except:
    print("error occurred when logging")
  awsController.add_log(next_log_id(), get_user_email(), "Sign-Out", logTime, logDetails)
  session.clear()
  return redirect("/")

if __name__ == "__main__":
  app.run(threaded=True)

