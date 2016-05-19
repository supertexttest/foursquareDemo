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
        response = request.getresponse()
        print (response.read())
        print(type(response))
        # print(response.id)
        # print (response.speech)

        payload = {'recipient': {'id': recipient_id},
                   'message': {'text': response.read()}
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