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
import datetime

from bot import Bot

app = Flask(__name__)
TOKEN = "EAAG9OSBpGwsBAEnbeuZAwQsksT5gJ3NsDAxtRkwJnGIJcUEli03CGqAmv9ZBoGnpwsyW7Vai8s8PYvyZCNRLUTQzxC2yBa3asrncqjmfiSwH9nLFPf3R74z2O1IpdSTWejcGOBuoeZBhcF0UPLT6thx8wCZCglefbaPHL88vQJhrZCGijfBwvr"
bot = Bot(TOKEN)

# import pickle
# Flask app should start in global layout
# app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)



@app.route("/webhook", methods = ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if (request.args.get("hub.verify_token") == "testbot_verify_token"):
                return request.args.get("hub.challenge")
    if request.method == 'POST':
        output = request.json
        event = output['entry'][0]['messaging']
        for x in event:
            if (x.get('message') and x['message'].get('text')):
                message = x['message']['text']
                recipient_id = x['sender']['id']
                bot.send_text_message(recipient_id, message)
            else:
                pass
        return "success"


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     req = request.get_json(silent=True, force=True)

#     print("Request:")
#     print(json.dumps(req, indent=4))

#     res = processRequest(req)

#     res = json.dumps(res, indent=4)
#     # print(res)
#     r = make_response(res)
#     r.headers['Content-Type'] = 'application/json'
#     # sys.stdout.write(r)
#     print(r)
#     return r


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
    if req.get("result").get("action") != "foursquareAPIsDemo   ":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    food_order = parameters.get("food_order")
    fun_activity = parameters.get("fun_activity")
    movie_activity = parameters.get("movie")
    given_address = parameters.get('area_bangalore')
    # sys.stdout.write(given_address)
    if food_order:
        file_in = open("objs.txt","wb")
        file_in.write(food_order)
        sys.stdout.write("1111")
        sys.stdout.write(food_order)
        sys.stdout.write("22222")
        file_in.close()
    if given_address:
        file_out = open("objs.txt","r")
        food_order = file_out.read()
        sys.stdout.write("3333")
        sys.stdout.write(given_address)
        sys.stdout.write(food_order)
        file_out.close()
        with open("objs.txt", "w"):
            pass

    google_map_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + given_address +"&key=AIzaSyDBxg0Go8biQLvb2O10zU8TomUalu2mK_g"
    sys.stdout.write(google_map_url)
    map_result = urllib.urlopen(google_map_url).read()
    map_data = json.loads(map_result)
    results = map_data.get('results')
    geometry = results[0].get('geometry').get('location')
    lat = geometry.get('lat')
    lng = geometry.get('lng')

    if fun_activity:
        query = fun_activity
    if food_order:
        query = food_order
    if movie_activity:
        query = movie_activity
    # baseurl = "https://api.foursquare.com/v2/venues/search?"
    baseurl = "https://api.foursquare.com/v2/venues/explore?"
    date = datetime.datetime.now().strftime ("%Y%m%d")
    if city:
        # yql_url = baseurl + "client_id=FBR415TEGJMA13MWR0ZXS2RD0KO1PBVEEFKBNPC5Y1K23FHQ&client_secret=EIGPMK3AV4IALOK4KJWIKJH1AA40R1KVKP2L3VY5O0TD5KBL&v=20130815&near=" + city + "&query=" + query + "&v=" + date
        yql_url = baseurl + "oauth_token=EMN1IAQ2TNZLHDI0VV3HSCKHWWLV3X3LGMKJV10KTBI55UDL&near=" + city + "&query=" + query + "&v=" + date

        
    else:
        # yql_url = baseurl + "client_id=FBR415TEGJMA13MWR0ZXS2RD0KO1PBVEEFKBNPC5Y1K23FHQ&client_secret=EIGPMK3AV4IALOK4KJWIKJH1AA40R1KVKP2L3VY5O0TD5KBL&v=20130815&ll="+str(lat)+","+str(lng)+"&query=" + query
        yql_url = baseurl + "oauth_token=EMN1IAQ2TNZLHDI0VV3HSCKHWWLV3X3LGMKJV10KTBI55UDL&ll="+str(lat)+","+str(lng)+"&query=" + query + "&v=" + date
    sys.stdout.write(yql_url)
    result = urllib.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResultExplore(data)
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
        if count > 2:
            break
        name = item.get('name')
        url = item.get('url')
        menu = item.get('menu')
        mobile_menu = ""
        menu_url = ""
        if menu:
            mobile_menu = menu.get('mobileUrl')
            menu_url = menu.get('url')
        location = item.get('location')
        address = location.get('address')
        if address:
            if mobile_menu != "":
                speech = speech + name + " and address is: " + address + " ,url : \n" + url + ",mobile menu is:" + mobile_menu + " , "
            elif menu_url != "":
                speech = speech + name + " and address is: " + address + " ,url : \n" + url + ",menu is:" + menu_url + " , "
            elif url:
                    speech = speech + name + " and address is: " + address + " ,url : \n" + url + " , "
            else:
                speech = speech + name + " and address is: " + address + " ,"
            count = count + 1
    speech_result = speech_default + speech

    print("Response:")
    print(speech_result)
    return {
        "speech": speech_result,
        "displayText": speech_result,
        "source": "apiai-weather-webhook-sample"
    }


def makeWebhookResultExplore(data):
    response = data.get('response')
    groups = response.get('groups')
    items = groups[0].get('items')
    speech_default = "Sure, I will find places near you. You can go to following places: "
    speech = ""
    count = 0
    for item in items:
        if count > 2:
            break
        venue = item.get('venue')
        name = venue.get('name')
        url = venue.get('url').encode('utf-8')
        menu = venue.get('menu')
        mobile_menu = ""
        menu_url = ""
        if menu:
            mobile_menu = menu.get('mobileUrl').encode('utf-8')
            menu_url = menu.get('url').encode('utf-8')
        location = venue.get('location')
        address = location.get('address')
        if address:
            if mobile_menu != "":
                speech = speech + name + " and address is: " + address + " and url :" + url + " and mobile menu is:" + mobile_menu + ", "
            elif menu_url != "":
                speech = speech + name + " and address is: " + address + " and url :" + url + " and menu is:" + menu_url + " , "
            elif url:
                speech = speech + name + " and address is: " + address + " and url :" + url + " , "
            else:
                speech = speech + name + " and address is: " + address + " ,"
            count = count + 1
    speech_result = speech_default + speech
    speech_result_final = speech_result.encode('utf-8')

    print("Response:")
    print(speech_result_final)
    return {
        "speech": speech_result_final,
        "displayText": speech_result_final,
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
    # handler = RotatingFileHandler('foursquare.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)

    app.run(debug=False, port=port, host='0.0.0.0') 