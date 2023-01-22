import boto.ses
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
import time
import string

global lastUserID
lastUserID = 0
global createNewUser
createNewUser = False



calendarTable = Table('STEAM-APP-Calendar', connection=conn)
clubsTable = Table('STEAM-APP-Clubs', connection=conn)
serviceTable = Table('STEAM-APP-Service', connection=conn)
userTable = Table('STEAM-APP-Users', connection=conn)
commTable = Table('STEAM-APP-Communication', connection=conn)
dayTable = Table('STEAM-APP-Day', connection=conn)
logTable = Table('STEAM-APP-Log', connection=conn)

def get_club_items():
    clubItems = clubsTable.scan()
    listItems = list(clubItems)
    itemsList = []
    itemDictionary = {}
    socialList = []
    for item in listItems:
        itemDictionary = {}
        socialList = []
        #create the item dictionary
        try:
            itemDictionary.update({"Club-Name" : item["name"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"ID" : item["id"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Dept" : item["Department"]})
        except:
            print("none of this type for object")
        try: 
            itemDictionary.update({"Description" : item["Description"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Leader" : item["Leader"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Location" : list(item["Location"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Meeting" : item["Meeting"]})
        except:
            print("none of this type for object")
        try:
            for network in item["Social"]:
                socialList.append(network)
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Social" : socialList})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Sponsor" : item["Sponsor"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Subtype" : item["Subtype"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Type" : str(item["Type"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Website" : item["Website"]})
        except:
            print("none of this type for object")
        itemsList.append(itemDictionary)
    return itemsList
def get_calendar_items():
    calendarItems = calendarTable.scan()
    listItems = list(calendarItems)
    itemsList = []
    itemDictionary = {}
    for item in listItems:
        itemDictionary = {}
        #create the item dictionary
        try:
            itemDictionary.update({"Event-Name" : item["name"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"ID" : item["id"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Club" : str(item["Club"])})
        except:
            print("none of this type for object")
        try: 
            itemDictionary.update({"Description" : item["Description"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"End-Date" : item["End-Date"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"End-Time" : item["End-Time"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Max-Attendees" : str(item["Max-Attendees"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Start-Date" : item["Start-Date"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Start-Time" : item["Start-Time"]})
        except:
            print("none of this type for object")
        itemsList.append(itemDictionary)
    return itemsList
def get_service_items():
    serviceItems = serviceTable.scan()
    listItems = list(serviceItems)
    itemsList = []
    itemDictionary = {}
    for item in listItems:
        itemDictionary = {}
        #create the item dictionary
        try:
            itemDictionary.update({"Service-Name" : item["name"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"ID" : str(item["id"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Club" : str(item["Club"])})
        except:
            print("none of this type for object")
        try: 
            itemDictionary.update({"Description" : item["Description"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"End-Date" : item["End-Date"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"End-Time" : item["End-Time"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Hours" : str(item["Hours"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Link" : item["Link"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Sign-Ups" : str(item["Sign-Ups"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Start-Date" : item["Start-Date"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Start-Time" : item["Start-Time"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Type" : item["Type"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"User-ID" : str(item["User-ID"])})
        except:
            print("none of this type for object")
        itemsList.append(itemDictionary)
    return itemsList
def get_comm_items():
    commItems = commTable.scan()
    listItems = list(commItems)
    itemsList = []
    itemDictionary = {}
    for item in listItems:
        itemDictionary = {}
        #create the item dictionary
        try:
            itemDictionary.update({"Club-ID" : item["clubid"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"ID" : item["id"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Announcement" : str(item["Announcement"])})
        except:
            print("none of this type for object")
        try: 
            itemDictionary.update({"Created-At" : item["Created-At"]})
        except:
            print("none of this type for object")
        try: 
            itemDictionary.update({"Creator" : item["Creator"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Message" : item["Message"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"To-Members" : list(item["To-Members"])})
        except:
            print("none of this type for object")
        itemsList.append(itemDictionary)
    return itemsList
def get_day_items():
    dayItems = dayTable.scan()
    listItems = list(dayItems)
    itemsList = []
    itemDictionary = {}
    for item in listItems:
        itemDictionary = {}
        try:
            itemDictionary.update({"Day" : item["day"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Type" : item["type"]})
        except:
            print("none of this type for object")
        itemsList.append(itemDictionary)
    return itemsList
def get_user_items():
    userItems = userTable.scan()
    listItems = list(userItems)
    itemsList = []
    itemDictionary = {}
    for item in listItems:
        itemDictionary = {}
        #create the item dictionary
        try:
            itemDictionary.update({"User-Name" : item["name"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"User-Email" : item["email"]})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Clubs-Joined" : list(item["Clubs-Joined"])})
        except:
            print("none of this type for object")
        try: 
            itemDictionary.update({"Clubs-Owned" : list(item["Clubs-Owned"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Hour-Total" : str(item["Hour-Total"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"ID" : str(item["ID"])})
        except:
            print("none of this type for object")
        try:
            itemDictionary.update({"Service" : list(item["Service"])})
        except:
            print("none of this type for object")
        itemsList.append(itemDictionary)
    return itemsList
def add_club(email, name, clubId):
    userAccount = userTable.get_item(name=name, email=email)
    userClubsArr = list(userAccount["Clubs-Joined"])
    userClubsArr.append(clubId)
    if (userClubsArr[0] == ""):
        userClubsArr.pop(0)
    userAccount["Clubs-Joined"] = userClubsArr
    userAccount.partial_save()
def add_club_owner(email, name, clubId):
    userAccount = userTable.get_item(name=name, email=email)
    userClubsArr = list(userAccount["Clubs-Owned"])
    userClubsArr.append(clubId)
    if (userClubsArr[0] == ""):
        userClubsArr.pop(0)
    userAccount["Clubs-Owned"] = userClubsArr
    userAccount.partial_save()
def remove_club(email, name, clubId):
    userAccount = userTable.get_item(name=name, email=email)
    userClubsArr = list(userAccount["Clubs-Joined"])
    userClubsArr.remove(clubId)
    if (len(userClubsArr) == 0):
        userClubsArr = [""]
    elif (userClubsArr[0] == ""):
        userClubsArr.pop(0)
    userAccount["Clubs-Joined"] = userClubsArr
    userAccount.partial_save()
def remove_club_owner(email, name, clubId):
    userAccount = userTable.get_item(name=name, email=email)
    userClubsArr = list(userAccount["Clubs-Owned"])
    userClubsArr.remove(clubId)
    if (len(userClubsArr) == 0):
        userClubsArr = [""]
    elif (userClubsArr[0] == ""):
        userClubsArr.pop(0)
    userAccount["Clubs-Owned"] = userClubsArr
    userAccount.partial_save()
def add_user_service(email, name, serviceId):
    userAccount = userTable.get_item(name=name, email=email)
    userServicesArr = list(userAccount["Service"])
    userServicesArr.append(serviceId)
    if (userServicesArr[0] == ""):
        userServicesArr.pop(0)
    userAccount["Service"] = userServicesArr
    userAccount.partial_save()
def remove_user_service(email, name, clubId):
    userAccount = userTable.get_item(name=name, email=email)
    userServiceArr = list(userAccount["Service"])
    userServiceArr.remove(clubId)
    if (len(userServiceArr) == 0):
        userServiceArr = [""]
    elif (userServiceArr[0] == ""):
        userServiceArr.pop(0)
    userAccount["Service"] = userServiceArr
    userAccount.partial_save()
def find_last_id():
    global lastUserID
    userItems = userTable.scan()
    listItems = list(userItems)
    for item in listItems:
        try:
            lastUserID = item["ID"]
        except:
            print("minor error")
def find_next_id():
    global lastUserID
    nextId = lastUserID + 1
    lastUserID = nextId
    return nextId
def find_user_name(email):
    name = ""
    userItems = userTable.scan()
    listItems = list(userItems)
    for item in listItems:
        if (item["email"] == email):
            name = item["name"]
    return name
def add_user(email, name, clubsJoined, clubsOwned, hourTotal, service, id=-1):
    if (id == -1):
        global createNewUser
        if (createNewUser == False):
            find_last_id()
            createNewUser = True
        id = find_next_id()
        userTable.put_item(data={
            "name" : name,
            "email" : email,
            "Clubs-Joined" : clubsJoined,
            "Clubs-Owned" : clubsOwned,
            "Hour-Total" : int(hourTotal),
            "ID" : int(id),
            "Service" : service
        })
    else:
        userTable.put_item(data={
            "name" : name,
            "email" : email,
            "Clubs-Joined" : clubsJoined,
            "Clubs-Owned" : clubsOwned,
            "Hour-Total" : int(hourTotal),
            "ID" : int(id),
            "Service" : service
        })
def rename_user(oldName, newName, email):
    userAccount = userTable.get_item(name=oldName, email=email)
    clubsJoined = userAccount["Clubs-Joined"]
    clubsOwned = userAccount["Clubs-Owned"]
    hourTotal = userAccount["Hour-Total"]
    id = userAccount["ID"]
    service = userAccount["Service"]
    add_user(email, newName, clubsJoined, clubsOwned, hourTotal, service, id)
    userTable.delete_item(name=oldName, email=email)
def new_user(email, name):
    add_user(email, name, [""], [""], 0, [""])
def check_user(email, userName="", justVerify=False):
    if ((find_user_name(email) == "") and (not justVerify)):
        ownerName = string.capwords(email.split("@")[0].replace(".", " "))
        if (userName != ""):
            ownerName = userName
        new_user(email, ownerName)
        return True
    elif (find_user_name(email) == ""):
        return False
    else:
        return True        
def edit_club_info(cName, clubId, description, leaders, location, meeting, social, sponsors, subtype, type, website, addOwners, removeOwners):
    clubAccount = clubsTable.get_item(name=cName, id=int(clubId))
    clubAccount["Description"] = description
    clubAccount["Leader"] = leaders
    clubAccount["Location"] = location
    clubAccount["Meeting"] = meeting
    clubAccount["Social"] = social
    clubAccount["Sponsor"] = sponsors
    clubAccount["Subtype"] = subtype
    clubAccount["Type"] = type
    clubAccount["Website"] = website
    clubAccount.partial_save()
    if (addOwners != [""]):
        for ownerItems in addOwners:
            check_user(ownerItems[0])
            add_club_owner(ownerItems[0], find_user_name(ownerItems[0]), clubId)
    if (removeOwners != [""]):
        for ownerItems in removeOwners:
            if (check_user(ownerItems[0], True)):
                remove_club_owner(ownerItems[0], find_user_name(ownerItems[0]), clubId)
def edit_club_member(membersAdd, membersRemove, clubId):
    if (len(membersAdd) > 0):
        if (membersAdd[0][0] != ""):
            for memberItem in membersAdd:
                memberEmail = memberItem[0]
                check_user(memberEmail)
                if (memberItem[1] == ""):
                    memberItem[1] = find_user_name(memberEmail)
                user = userTable.query_2(name__eq = memberItem[1], email__eq = memberItem[0])
                for userItem in user:
                    add_club(userItem["email"], userItem["name"], clubId)
    if (len(membersRemove) > 0):
        if (membersRemove[0][0] != ""):
            for memberItem in membersRemove:
                memberEmail = memberItem[0]
                if (check_user(memberEmail, True)):
                    user = userTable.query_2(name__eq = memberItem[1], email__eq = memberEmail)
                    for userItem in user:
                        remove_club(userItem["email"], userItem["name"], clubId)
def check_event(eventInfo):
    try:
        eventItem = calendarTable.get_item(name=eventInfo["Event-Name"], id=int(eventInfo["ID"]))
        return True
    except:
        return False
def add_event(name, id, club, description, endDate, endTime, maxAttend, startDate, startTime):
    calendarTable.put_item(data={
        "name" : name,
        "id" : int(id),
        "Club" : club,
        "Description" : description,
        "End-Date" : endDate,
        "End-Time" : endTime,
        "Max-Attendees" : int(maxAttend),
        "Start-Date" : startDate,
        "Start-Time" : startTime
    })
def delete_event(name, id):
    calendarTable.delete_item(name=name, id=int(id))
def update_event(oldName, newName, id, club, description, endDate, endTime, maxAttend, startDate, startTime):
    eventItem = calendarTable.get_item(name=oldName, id=int(id))
    parsedNewName = newName.find("DELETE")
    if (newName == ""):
        eventItem["Description"] = description
        eventItem["End-Date"] = endDate
        eventItem["End-Time"] = endTime
        eventItem["Start-Date"] = startDate
        eventItem["Start-Time"] = startTime
        eventItem["Max-Attendees"] = int(maxAttend)
        eventItem.partial_save()
    elif (parsedNewName != -1):
        delete_event(oldName, id)
    else:
        add_event(newName, id, club, description, endDate, endTime, maxAttend, startDate, startTime)
        calendarTable.delete_item(name=oldName, id=int(id))
def edit_club_event(updateEvents):
    for event in updateEvents:
        try:
            if (check_event(event)):
                update_event(event["Event-Name"], event["Change-Name"], event["ID"], event["Club"], event["Description"], event["End-Date"], event["End-Time"], event["Max-Attendees"], event["Start-Date"], event["Start-Time"])
            else:
                add_event(event["Change-Name"], event["ID"], event["Club"], event["Description"], event["End-Date"], event["End-Time"], event["Max-Attendees"], event["Start-Date"], event["Start-Time"])
        except:
            print("had error uploading to database")
def check_service(serviceInfo):
    try:
        serviceItem = serviceTable.get_item(name=serviceInfo["Service-Name"], id=int(serviceInfo["ID"]))
        return True
    except:
        return False
def edit_service_member(membersAdd, membersRemove, serviceId):
    if (len(membersAdd) > 0):
        if (membersAdd[0][0] != ""):
            for memberItem in membersAdd:
                memberEmail = memberItem[0]
                check_user(memberEmail)
                if (memberItem[1] == ""):
                    memberItem[1] = find_user_name(memberEmail)
                user = userTable.query_2(name__eq = memberItem[1], email__eq = memberItem[0])
                for userItem in user:
                    add_user_service(userItem["email"], userItem["name"], serviceId)
    if (len(membersRemove) > 0):
        if (membersRemove[0][0] != ""):
            for memberItem in membersRemove:
                memberEmail = memberItem[0]
                if (check_user(memberEmail, True)):
                    user = userTable.query_2(name__eq = memberItem[1], email__eq = memberEmail)
                    for userItem in user:
                        remove_user_service(userItem["email"], userItem["name"], serviceId)
def add_service(name, id, club, description, endDate, endTime, hours, startDate, startTime, signUps, link, type, userId, signUpPeople):
    serviceTable.put_item(data={ 
        "name" : name,
        "id" : int(id),
        "Club" : int(club),
        "Description" : description,
        "End-Date" : endDate,
        "End-Time" : endTime,
        "Hours" : int(hours),
        "Start-Date" : startDate,
        "Start-Time" : startTime,
        "Sign-Ups" : int(signUps),
        "Link" : link,
        "Type" : type,
        "User-ID" : int(userId)
    })
    edit_service_member(signUpPeople["Members-Add"], signUpPeople["Members-Remove"], id)
def delete_service(name, id):
    serviceTable.delete_item(name=name, id=int(id))
def update_service(oldName, newName, id, club, description, endDate, endTime, hours, startDate, startTime, signUps, link, type, userId, signUpPeople):
    serviceItem = serviceTable.get_item(name=oldName, id=int(id))
    parsedNewName = newName.find("-DELETE")
    if (newName == ""):
        serviceItem["Description"] = description
        serviceItem["End-Date"] = endDate
        serviceItem["End-Time"] = endTime
        serviceItem["Start-Date"] = startDate
        serviceItem["Start-Time"] = startTime
        serviceItem["Sign-Ups"] = int(signUps)
        serviceItem["Hours"] = int(hours)
        serviceItem["Link"] = link
        serviceItem["Type"] = type
        serviceItem["User-ID"] = int(userId)
        serviceItem.partial_save()
        edit_service_member(signUpPeople["Members-Add"], signUpPeople["Members-Remove"], id)
    elif (parsedNewName != -1):
        delete_service(oldName, id)
    else:
        add_service(newName, id, club, description, endDate, endTime, hours, startDate, startTime, signUps, link, type, userId, signUpPeople)
        serviceTable.delete_item(name=oldName, id=int(id))
def edit_club_service(updateServices):
    for service in updateServices:
        try:
            if (check_service(service)):
                update_service(service["Service-Name"], service["Change-Name"], service["ID"], service["Club"], service["Description"], service["End-Date"], service["End-Time"], service["Hours"], service["Start-Date"], service["Start-Time"], service["Sign-Ups"], service["Link"], service["Type"], service["User-ID"], service["Sign-Up-People"])
            else:
                add_service(service["Change-Name"], service["ID"], service["Club"], service["Description"], service["End-Date"], service["End-Time"], service["Hours"], service["Start-Date"], service["Start-Time"], service["Sign-Ups"], service["Link"], service["Type"], service["User-ID"], service["Sign-Up-People"])
        except:
            print("had error uploading to database")
def check_notif(notifInfo):
    try:
        notifItem = commTable.get_item(clubid=int(notifInfo["Club-ID"]), id=int(notifInfo["ID"]))
        return True
    except:
        return False
def update_notif(id, club, announcement, createdAt, message, toMembers, delete):
    if (delete):
        commTable.delete_item(clubid=int(club), id=int(id))
    else: 
        notifItem = commTable.get_item(clubid=int(club), id=int(id))
        notifItem["Announcement"] = announcement
        notifItem["Message"] = message
        notifItem["To-Members"] = list(toMembers)
        if (createdAt != "n/a"):
            notifItem["Created-At"] = createdAt
        notifItem.partial_save()
def add_notif(id, club, announcement, createdAt, creator, message, toMembers):
    commTable.put_item(data={ 
        "clubid" : int(club),
        "id" : int(id),
        "Announcement" : announcement,
        "Created-At" : createdAt,
        "Creator" : creator,
        "Message" : message,
        "To-Members" : list(toMembers)
    })
def edit_club_communication(updateComms):
    for notif in updateComms:
        try:
            if (check_notif(notif)):
                update_notif(notif["ID"], notif["Club-ID"], notif["Announcement"], notif["Created-At"], notif["Message"], notif["To-Members"], notif["Delete"])
            else:
                add_notif(notif["ID"], notif["Club-ID"], notif["Announcement"], notif["Created-At"], notif["Creator"], notif["Message"], notif["To-Members"])
        except:
            print("had error uploading to database")
def add_log(logId, userEmail, logType, logTime, logDetails):
    logTable.put_item(data={
        "id" : int(logId),
        "userid" : userEmail,
        "Time" : logTime,
        "Type" : logType,
        "Details" : logDetails
    })
    print("logged event")
def last_log_id():
    logItems = logTable.scan()
    listItems = list(logItems)
    lastId = 0
    for item in listItems:
        thisId = int(item["id"])
        if (thisId > lastId):
            lastId = thisId
    return lastId