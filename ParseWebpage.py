import urllib.request
import bs4 as bs
import requests
from twilio.rest import Client
import time

def sendEmail(data):
    try:
        f = open('mailgun.key')
        key = f.read()
        f.close()
    except IOError:
        print("Mailgun API key missing")
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd10bb35ab0c4461aabdc94d6fce977ac.mailgun.org/messages",
        auth=("api", key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd10bb35ab0c4461aabdc94d6fce977ac.mailgun.org>",
            "to": "lance.e.jordan@gmail.com",
            "subject": data,
            "text": data})

def sendSMS(data):
    try:
        f = open('twilio.key')
        auth_token = f.read()
        f.close()
    except IOError:
        print("Twilio API key missing")
    account_sid = 'AC5a814c3a42f034a8f0aeca0f0539743f'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                         body=data,
                         from_='+12816231670', #Twilio phone number
                         to='+12818535023' #Lance's phone number
                     )

    return message.sid

def getClassData(classID):
    try:
        infile = urllib.request.urlopen("https://myeagle.hccs.edu/app/catalog/classsection/HCCSD/6211/" + classID)
    except:
        pass
    return infile.read().decode()

def parseOpenSpots(data):
    soup = bs.BeautifulSoup(data, 'html.parser')

    divSoup = soup.findAll("div", class_="section-content clearfix")
    openSpots = divSoup[16].findAll('div')[3].get_text()
    return openSpots

def openClass(classID):
    sendSMS("Open class " + classID + "!!!")
    sendEmail("Open class " + classID + "!!!")

#Class IDs
classList = ["24550","13492","15081","12723","15075","10642","12702"]

while True:
    for classID in classList:
        data = getClassData(classID)
        spots = parseOpenSpots(data)
        print(classID, spots)
        if spots != "0":
            print("Class found!!!\nClass ID: " + classID)
            openClass(classID)
    time.sleep(3600)
