import requests
import json
from apiai import ApiAI
import datetime
import urllib

CLIENT_ACCESS_TOKEN = '4f176853c63c4d1897b4c3c1b44b6040'
ai = ApiAI(CLIENT_ACCESS_TOKEN)
class Bot:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v2.6/me/messages?access_token={0}".format(access_token)

    def generic_message(self,recipient_id,text):
        imageUrl = "https://placekitten.com/200/300"
        message = {
                  "attachment": {
                      "type": "template",
                      "payload": {
                          "template_type": "generic",
                          "elements": [{
                              "title": "Kitten",
                              "subtitle": "Cute kitten picture",
                              "image_url": imageUrl ,
                              "buttons": [{
                                  "type": "web_url",
                                  "url": imageUrl,
                                  "title": "Show kitten"
                                  }, {
                                  "type": "postback",
                                  "title": "I like this",
                                  "payload": "User " + recipient_id + " likes kitten " + imageUrl
                              }]
                          }]
                      }
                  }
              }
        print(message)
        result = requests.post(self.base_url, json=message)
        return result.json()

    def send_generic_message1(self, recipient_id, elements):
        imageUrl = "https://placekitten.com/200/300"
        payload = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                          "elements": [{
                              "title": "Kitten",
                              "subtitle": "Cute kitten picture",
                              "image_url": imageUrl,
                              "buttons": [{
                                "type": "web_url",
                                "url": imageUrl,
                                "title": "Show kitten"
                                }]
                          },{
                              "title": "Kitten",
                              "subtitle": "Cute kitten picture",
                              "image_url": imageUrl,
                              "buttons": [{
                                "type": "web_url",
                                "url": imageUrl,
                                "title": "Show kitten"
                                }]
                          },
                          {
                              "title": "Kitten",
                              "subtitle": "Cute kitten picture",
                              "image_url": imageUrl,
                              "buttons": [{
                                "type": "web_url",
                                "url": imageUrl,
                                "title": "Show kitten"
                                }]
                          }]
                    }
                }
            }
        }
        return self._send_payload(payload)

    def send_generic_message(self,recipient_id, query):

        baseurl = "https://api.foursquare.com/v2/venues/explore?"
        date = datetime.datetime.now().strftime ("%Y%m%d")
        yql_url = baseurl + "query="+query+"&ll=40.7,-74&oauth_token=EMN1IAQ2TNZLHDI0VV3HSCKHWWLV3X3LGMKJV10KTBI55UDL&v=20160516"
        print(yql_url)
        # if city:
        #     yql_url = baseurl + "oauth_token=EMN1IAQ2TNZLHDI0VV3HSCKHWWLV3X3LGMKJV10KTBI55UDL&ll=40.7,-74" + city + "&query=" + query + "&v=" + date
        # else:
        #     yql_url = baseurl + "oauth_token=EMN1IAQ2TNZLHDI0VV3HSCKHWWLV3X3LGMKJV10KTBI55UDL&ll="+str(lat)+","+str(lng)+"&query=" + query + "&v=" + date
        # sys.stdout.write(yql_url)
        result = urllib.urlopen(yql_url).read()
        data = json.loads(result)
        # res = makeWebhookResultExplore(data)
        response = data.get('response')
        groups = response.get('groups')
        items = groups[0].get('items')
        speech_default = "Sure, I will find places near you. You can go to following places: "
        speech = ""
        count = 0
        for item in items:
            if count > 0:
                break
            venue = item.get('venue')
            name = venue.get('name')
            url = venue.get('url').encode('utf-8')
            # menu = venue.get('menu')
            # mobile_menu = ""
            # menu_url = ""
            # if menu:
            #     mobile_menu = menu.get('mobileUrl').encode('utf-8')
            #     menu_url = menu.get('url').encode('utf-8')
            location = venue.get('location')
            address = location.get('address')
            count = count +1
        text_message = name + ", "+url+", "+address
        print(text_message)

        payload = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                          "elements": [{
                              "title": name,
                              "subtitle": address,
                              "image_url": url,
                              "buttons": [{
                                "type": "web_url",
                                "url": url,
                                "title": "Show "+name
                                }]
                          }]
                    }
                }
            }
        }
        return self._send_payload(payload)
        payload = {'recipient': {'id': recipient_id},
                   'message': {'text':text_message
                              }
                   }
        result = requests.post(self.base_url, json=payload)
        return result.json()

    def send_text_message(self, recipient_id, message):
        payload = {'recipient': {'id': recipient_id},
                   'message': {'text': message}
                  }
        result = requests.post(self.base_url, json=payload)
        return result.json()
    def send_text_message_api_ai(self, recipient_id, text):
        print("insideeeeeeeeee oneeeeeeeeeeeee")
        file_out = open("objs_server.txt","r")
        food_order = file_out.read()
        print("food_order is:"+food_order)
        file_out.close()
        with open("objs_server.txt", "w"):
            pass
        if food_order != "":
          print("inside foursquare api codeeeeeeeeeee")
          self.generic_message(recipient_id,food_order)
        else:
          print("inside elseeeeeeeeeeee")
          request = ai.text_request()
          request.lang = 'en'  # optional, default value equal 'en'
          request.query = text
          response = request.getresponse()
    
          string = response.read().decode('utf-8')
          print(string)
          # string_string = str(string)
          # string_dump = json.dumps(string)
          food_order = ""
          area_bangalore = ""
          low = string.find('food_order')
          print(low)
          if low != -1:
            high = string.find('"',low+14)
            if (high - low) > 1:
              print("inside food_order to write into file")
              food_order = string[low+14:high]
          print(food_order)
          # low_add = string.find('area_bangalore')
          # if low_add != -1:
          #   high_add = string.find('"',low_add+18)
          #   if (high_add - low_add) > 1:
          #     area_bangalore = string[low_add:high_add]

          if food_order != "":
            print('writing into fileee: '+food_order)
            file_in = open("objs_server.txt","wb")
            file_in.write(food_order)
            file_in.close()
          # if area_bangalore != "":
          #   file_out = open("objs_server.txt","r")
          #   food_order = file_out.read()
          #   file_out.close()
          #   with open("objs_server.txt", "w"):
          #       pass
          
          index_start = string.find('speech')
          # print(index_start)
          index_end = string.find('}',index_start)
          final_string = string[index_start+9:index_end-1]
          print(final_string)

          payload = {'recipient': {'id': recipient_id},
                     'message': {'text': final_string}
                    }
          result = requests.post(self.base_url, json=payload)
          return result.json()
   
    def send_message(self, recipient_id, message):
        payload ={'recipient': {'id': recipient_id},
                  'message': message
                 }
        return requests.post(self.base_url, json=payload).json()

    def _send_payload(self, payload):
        result = requests.post(self.base_url, json=payload).json()
        return result

    



      