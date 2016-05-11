#!/usr/bin/env python

import urllib
import json
import os


from flask import Flask
from flask import request
from flask import make_response

from flask import render_template
import sys
import logging

# Flask app should start in global layout
app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# def processRequest(req):
#     if req.get("result").get("action") != "yahooWeatherForecast":
#         return {}
#     baseurl = "https://query.yahooapis.com/v1/public/yql?"
#     yql_query = makeYqlQuery(req)
#     if yql_query is None:
#         return {}
#     yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
#     result = urllib.urlopen(yql_url).read()
#     data = json.loads(result)
#     res = makeWebhookResult(data)
#     return res

def processRequest(req):
    if req.get("result").get("action") != "foursquareAPIsDemo":
        return {}
    baseurl = "https://api.foursquare.com/v2/venues/search?"
    yql_url = baseurl + "client_id=FBR415TEGJMA13MWR0ZXS2RD0KO1PBVEEFKBNPC5Y1K23FHQ&client_secret=EIGPMK3AV4IALOK4KJWIKJH1AA40R1KVKP2L3VY5O0TD5KBL&v=20130815&ll=40.7,-74&query=sushi&format=json"
    sys.stdout.write(yql_url)
    result = urllib.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


# def makeYqlQuery(req):
#     result = req.get("result")
#     parameters = result.get("parameters")
#     city = parameters.get("geo-city")
#     if city is None:
#         return None

#     return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


# def makeWebhookResult(data):
#     query = data.get('query')
#     if query is None:
#         return {}

#     result = query.get('results')
#     if result is None:
#         return {}

#     channel = result.get('channel')
#     if channel is None:
#         return {}

#     item = channel.get('item')
#     location = channel.get('location')
#     units = channel.get('units')
#     if (location is None) or (item is None) or (units is None):
#         return {}

#     condition = item.get('condition')
#     if condition is None:
#         return {}

#     # print(json.dumps(item, indent=4))

#     speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
#              ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

#     print("Response:")
#     print(speech)

#     return {
#         "speech": speech,
#         "displayText": speech,
#         # "data": data,
#         # "contextOut": [],
#         "source": "apiai-weather-webhook-sample"
#     }


def makeWebhookResult(data):
    response = data.get('response')
    venues = response.get('venues')
    speech_default = "Sure, I will find places near you. You can go to following places: "
    speech = ""
    count = 0
    for item in venues:
        if count > 3:
            break
        name = item.get('name')
        location = item.get('location')
        address = location.get('address')
        speech = speech + name + " and address is: " + address + ", "
        count = count +1
    speech_result = speech_default + speech

    print("Response:")
    print(speech_result)
    return {
        "speech": speech_result,
        "displayText": speech_result,
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
    # handler = RotatingFileHandler('foursquare.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)

    app.run(debug=False, port=port, host='0.0.0.0')