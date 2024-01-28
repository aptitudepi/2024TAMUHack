#!/usr/bin/python3
from types import TracebackType
from flask import Flask, render_template, request, Response, jsonify, abort, request_started, session, redirect, url_for
#from flask_session import Session
#import awsController
import json
import secrets
import binascii
import math
import time
import os
from datetime import datetime, timezone, timedelta
#from oauthlib.oauth2 import WebApplicationClient
import requests
import cachecontrol
import pathlib
import string
import pytz

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.secret_key = "littlekey"

verifyCount = 0
lastIpIndex = 0
page = 0

#make sure user is logged in for certain pages
def voice_login_is_required(function):
  def wrapper(*args, **kwargs):
    if (("User" not in session) or ("Pass" not in session)):
      return abort(403) # forbidden
    else:
      return function()
  return wrapper
def dashboard_login_is_required(function):
  def wrapperm(*args, **kwargs):
    if (("User" not in session) or ("Pass" not in session)):
      return abort(403) # forbidden
    else:
      return function()
  return wrapperm
def management_login_is_required(function):
  def wrappern(*args, **kwargs):
    if (("User" not in session) or ("Pass" not in session)):
      return abort(403) # forbidden
    else:
      return function()
  return wrappern

def verifyLogin(enteredData):
  global verifyCount
  verifyCount = verifyCount + 1
  print("verify count:")
  print(verifyCount)
  dataFile = open('static/userData.json')
  users = json.load(dataFile)
  for user in users["users"]:
    if (user["user"] == enteredData["User"] and user["pass"] == enteredData["Pass"]):
      # user verified to be valid!
      verifyCount = 0
      session["User"] = user["user"]
      session["Pass"] = user["pass"]
      return True
  print("false login")
    
def get_user_device_data():
  dataFile = open('static/userData.json')
  users = json.load(dataFile)
  for user in users["users"]:
    if (user["user"] == session["User"] and user["pass"] == session["Pass"]):
      return [user["vendorId"], user["deviceName"], user["deviceManName"]]

def get_last_ip_index():
  global lastIpIndex
  with open("static/bannedIps.json", "r+") as dataFile:
    ipData = json.load(dataFile)
    for ipEntry in ipData["banned"]:
      ipIndex = ipEntry.keys()[0]
      # come back to debugging this later, throws bad error if user enters bad password thrice
      lastIpIndex = int(ipIndex)
def add_banned_ip(bannedIp):
  global lastIpIndex
  get_last_ip_index()
  with open("static/bannedIps.json", "r+") as dataFile:
    ipData = json.load(dataFile)
    lastIpIndex = lastIpIndex + 1
    nextIpString = str(lastIpIndex)
    ipData["banned"][nextIpString] = bannedIp
def is_banned_ip(bannedIp):
  with open("static/bannedIps.json", "r+") as dataFile:
    ipData = json.load(dataFile)
    index = 0
    for ipEntry in ipData["banned"]:
      strIndex = str(index)
      if (ipEntry[strIndex] == bannedIp):
        #the ip inputted is banned, so return true
        return True
      index = index + 1
  return False

def get_now():
  central = pytz.timezone('US/Central')
  return datetime.now(central).strftime("%d/%m/%Y %H:%M:%S")

@app.route("/", methods=['POST', 'GET'])
def initial_login():
  global verifyCount
  global page
  device_data = get_user_device_data()
  if (is_banned_ip(request.remote_addr)):
    return redirect("/unauthorized")
  if (request.method == "POST"):
    loginInfo = request.get_json()
    verifyLogin(loginInfo)
    print(verifyCount)
    if ("User" in session and "Pass" in session):
      if (session["User"] == loginInfo["User"] and session["Pass"] == loginInfo["Pass"]):
        print("here")
        page = 1
    if (verifyCount == 3):
      print("ip")
      print(request.remote_addr)
      add_banned_ip(request.remote_addr)
      return abort(401)
    print("did not work, entered:")
    print(loginInfo)
  return render_template("initial_login.html",  vendorId=device_data[0], deviceName=device_data[1], deviceManName=device_data[2], pageNumber=page)

@app.route("/help")
def route_help():
  if (is_banned_ip(request.remote_addr)):
    return redirect("/unauthorized")
  return render_template("help.html")

@app.route("/privacy-policy")
def route_privacy():
  return render_template("privacy.html")

@app.route("/terms")
def route_terms():
  return render_template("terms.html")

@app.route("/dashboard")
@dashboard_login_is_required
def route_dashboard():
  return render_template("dashboard.html")

@app.errorhandler(401)
def access_denied(error):
  return render_template('401.html', title='401'), 401

@app.errorhandler(403)
def page_forbidden(error):
  return render_template('403.html', title='403'), 403

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html', title='404'), 404

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
      print("add owners: ",editInfo["Add-Owners"])
      print("remove owners: ",editInfo["Remove-Owners"])
      editMembers = editData["Member"]
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
    except:
      print("not club data")
    try:
      editEvents = editData["Events"]
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
    except:
      print("not event data")
    try:
      editServices = editData["Services"]
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
    except:
      print("not service data")
    try:
      editComms = editData["Communication"]
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
    except:
      print("not service data")
  return render_template("management.html")

if __name__ == "__main__":
  app.run(threaded=True)

