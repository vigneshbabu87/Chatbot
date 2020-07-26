import json

import requests
from flask import Flask, render_template, jsonify
from flask import make_response
from flask import request
from flask_mail import Mail, Message
import time
import os
import smtplib  # import SMTP lib

# Flask app should start in global layout
app = Flask(__name__)

# configuration mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'viewpowerbi@gmail.com'
app.config['MAIL_PASSWORD'] = 'Test@123'

app.config['MAIL_DEFAULT_SENDER'] = 'viewpowerbi@gmail.com'
mail = Mail(app)


################################################

@app.route('/')
def home():
    return render_template('mail_template.html')


# create a route for webhook and calling from googledialogflow
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


@app.route('/staticreply', methods=['POST'])
def staticreply():
    speech = "Thanks for the message"
    myresultsdata = {
        "speech": speech,
        "displayText": speech,
        # "data": {},
        # "contextOut": [],
        "source": "TEstwebhook"
    }

    res = json.dumps(myresultsdata, indent=4)
    # res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# Calling API integration
# function for responses
def results():
    # build a request object
    req = request.get_json()
    username = None
    if request.method == "GET":
        print("GETmethod")
        print(req)
    elif request.method == "POST":
        dict = req;
        # getting parameters from server
        Districtwiseresults = ""
        username = dict["queryResult"]["parameters"]["any"]
        emailid = dict["queryResult"]["parameters"]["email"]
        phonenumber = dict["queryResult"]["parameters"]["phone-number"]
        zipcode = dict["queryResult"]["parameters"]["zip-code"]
        results = username + emailid + phonenumber
        print(results)

        datanew = callingAPI()

        #print("datareceived")
        #print(datanew)

        dataval = datanew

        Recovered = dataval['total_values']['recovered']
        Deaths = dataval['total_values']['deaths']
        Confirmed = dataval['total_values']['confirmed']
        #  Location = dataval['total_values']['location']
        Lastupdated = dataval['total_values']['lastupdatedtime']
        Active = dataval['total_values']['active']

        Mergedata = "Covid 19 overall status \n " + "\n Confirmed+\t:" + str(Confirmed) + "\n Active \t: " + str(
            Active) + "\n Recovered \t: " + str(
            Recovered) + "\n Deaths\t:" + str(Deaths) + "\n Lastupdated\t:" + str(Lastupdated)
        strname = "Thanks for sharing information " + results + "" + ",This is bot . Especially designed for covid19 " + Mergedata

        # passing user input zipcode to get teh COVID 19 details
        CovidreturnedVal = GetDistrictandstateusingpincode(zipcode)
        CovidreturnedValues = CovidreturnedVal
        send_mail(emailid, CovidreturnedValues)
        #print(str(CovidreturnedValues['Confirmed']))
        if ((int(CovidreturnedValues['Confirmed']) >= 0)):
            # results
            Districtwiseresults = "Please find the details for Covid 19 in your location " + str(
                CovidreturnedValues['District']) + " / " + str(
                CovidreturnedValues['State']) + "." + "\n Confirmed Cases \t:" + str(
                CovidreturnedValues['Confirmed']) + "\n Active Cases\t:" + str(
                CovidreturnedValues['Active']) + "\n Recovered Cases\t: " + str(
                CovidreturnedValues['Recovered']) + "\n Deceased Cases \t:" + str(CovidreturnedValues['Deceased'])

            Districtwiseresults = Districtwiseresults + "Requested details has been shared through mail.Please Proceed COVID 19 related queries."
            # sending mail to the user
           # send_mail(emailid, CovidreturnedValues)
        else:
            Districtwiseresults = {"State": "ALL", "District": "ALL", "Confirmed": Confirmed,
                                   "Active": "-", "Recovered": Recovered,
                                   "Deceased": Deaths}
            # sending mail to the user
           # send_mail(emailid, CovidreturnedValues)

    #print(Districtwiseresults)
    return {'fulfillmentText': Districtwiseresults}


# create a route for webhook
# @app.route('/webhook', methods=['GET', 'POST'])
# def webhook():
# return response
#   return make_response(jsonify(results()))


@app.route('/API', methods=['GET'])
def API():
    return make_response(jsonify(callingAPI()))


# Get the Overall Status
def callingAPI():
    params = {"country": "India"}
    # reponse = requests.get("https://api.covid19india.org/data.json")
    response = requests.get("https://corona-virus-world-and-india-data.p.rapidapi.com/api_india",
                            headers={
                                "X-RapidAPI-Host": "corona-virus-world-and-india-data.p.rapidapi.com",
                                "X-RapidAPI-Key": "c3c757f65emshd17f87cbb5ee540p1c2de2jsn4c33a76a8f0d"
                            })

    # print(response.json)
    if (response.status_code == 200):
        print(response.status_code)
        data = response.json()
        # data = requests.get_json("https://api.covid19india.org/data.json")
       # print("completed")
      #  print(data)
    return data


@app.route('/test', methods=['GET', 'POST'])
def test():
    return "test data"


@app.route("/data")
def sentmails():
    print("calling mail")
    CovidreturnedValues = {"State": "0", "District": "0", "Confirmed": "0",
                           "Active": "0", "Recovered": "0",
                           "Deceased": "0"}
    return make_response(jsonify(send_mail("vigneshb@pellucidinc.com", CovidreturnedValues)))


# Sending mail
def send_mail(recipients, covidreturnedval):
    print(app.config['MAIL_USERNAME'])
    try:
        msg = Message(
            sender=app.config['MAIL_USERNAME'],
            recipients=[recipients]
        )
        CovidreturnedValues = covidreturnedval
        print(CovidreturnedValues)

        stateval = CovidreturnedValues['State']
        print("state:" + stateval)
        districtval = CovidreturnedValues['District']
        Confirmedval = CovidreturnedValues['Confirmed']
        Activeval = CovidreturnedValues['Active']
        Recoveredval = CovidreturnedValues['Recovered']
        deceasedval = CovidreturnedValues['Deceased']

        msg.subject = "Covid 19 details"
        msg.body = 'Covid 19 details'
        msg.html = 'Thank you for sharing information.' + render_template('mail_template.html', state=stateval,
                                                                          District=districtval, Confirmed=Confirmedval,
                                                                          Active=Activeval,
                                                                          recovered=Recoveredval,
                                                                          deceased=deceasedval)
        #   Attachementpath=os.path.dirname(app.instance_path)+"\document\FAQ_COIVD.pdf"
        #  print(os.path.dirname(app.instance_path))
        #  with app.open_resource(Attachementpath) as fp:
        #         msg.attach("FAQ_COIVD.pdf", "FAQ_COIVD.pdf", fp.read())
        mail.send(msg)
        print("MAil sent")
    except Exception as e:
        print(e)
    # mail = Mail(app)
    # msg = Message('Hello', sender='viewpowerbi@gmail.com', recipients='m.vigneshbabu@gmail.com',)
    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    return "Sent"


@app.route('/pincode', methods=['GET'])
def CallingPincode():
    return make_response((GetDistrictandstateusingpincode("600001")))


def GetDistrictandstateusingpincode(pincode):
    APILink = "http://www.postalpincode.in/api/pincode/" + pincode
    response = requests.get(APILink)

    # print(response.json)
    if (response.status_code == 200):
        print(response.status_code)
        data = response.json()
        # data = requests.get_json("https://api.covid19india.org/data.json")
        #print(data)
        Districtdetails = data['PostOffice'][0]['District']
        Statedetails = data['PostOffice'][0]['State']
        print(Statedetails)
        print(Districtdetails)

        Covdetails = GetCovid19details(Statedetails, Districtdetails)
    #  render_template('mail_template.html', data=Cddetails)
    # return render_template('mail_template.html', state=Statedetails,District=Districtdetails,Confirmed=Covdetails['Confirmed'],Active=Covdetails['Active'],recovered=Covdetails['Recovered'],deceased=Covdetails['Deceased'])
    return Covdetails


def GetCovid19details(stateVal, DistrictVal):
    APILink = "https://api.covid19india.org/v2/state_district_wise.json"
    response = requests.get(APILink)
    Coviddetails = response.json()
    CovidreturnedValues = {}
    statevalues = stateVal
    districtvalues = DistrictVal
    #print("Coviddetails")
    #print(statevalues)
    #print(districtvalues)
    #print("------\n")
    index = -1
    districtindex = -1
    for statedet in Coviddetails:
        index = index + 1
        state = statedet['state']
        # print(state + statevalues)
        if statevalues == state:
             # print(Coviddetails[index]['districtData'])
            for val in Coviddetails[index]['districtData']:
                    #print(val['district'])
                if val['district'] == districtvalues:
                    Valconfirmedcases = int(val['confirmed']) + int(val['delta']['confirmed'])
                    valDeceased = int(val['deceased']) + int(val['delta']['deceased'])
                    ValRecovered = int(val['recovered']) + int(val['delta']['recovered'])
                    CovidreturnedValues = {"State": stateVal, "District": DistrictVal, "Confirmed": Valconfirmedcases,
                                           "Active": val['active'], "Recovered": ValRecovered,
                                           "Deceased": valDeceased}

                    break;

    return CovidreturnedValues


port = os.getenv("PORT")
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
   # app.run(host='127.0.0.1', port=8001, debug=True)
