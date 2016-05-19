import requests
import json
from apiai import ApiAI

CLIENT_ACCESS_TOKEN = '4f176853c63c4d1897b4c3c1b44b6040'
ai = ApiAI(CLIENT_ACCESS_TOKEN)
class Bot:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v2.6/me/messages?access_token={0}".format(access_token)

    def send_text_message(self, recipient_id, message):
        payload = {'recipient': {'id': recipient_id},
                   'message': {'text': message}
                  }
        result = requests.post(self.base_url, json=payload)
        return result.json()
    def send_text_message_api_ai(self, recipient_id, text):
        
        request = ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'
        request.query = text
        print(request.read())
        response = request.getresponse()
       
        string = response.read().decode('utf-8')
        print(string)
        # string_string = str(string)
        # string_dump = json.dumps(string)
        # food_order = ""
        # area_bangalore = ""
        # low = string.find('food_order')
        # if low != -1:
        #   high = string.find('"',low+14)
        #   if (high - low) > 1:
        #     food_order = string[low:high]

        # low_add = string.find('area_bangalore')
        # if low_add != -1:
        #   high_add = string.find('"',low_add+18)
        #   if (high_add - low_add) > 1:
        #     area_bangalore = string[low_add:high_add]

        # if food_order:
        #   file_in = open("objs_server.txt","wb")
        #   file_in.write(food_order)
        #   file_in.close()
        # if area_bangalore:
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

    def send_generic_message(self, recipient_id, elements):
        payload = {'recipient': {'id': recipient_id},
                   'message': { "attachment": {
                                "type": "template",
                                "payload": {
                                    "template_type": "generic",
                                    "elements": elements
                                    }
                                }
                              }
                   }
        return requests.post(self.base_url, json=payload).json()