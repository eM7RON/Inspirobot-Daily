import datetime
import requests
import sys

import slack_sdk

from secrets import CHANNEL_ID, TOKEN # python script containing secret tokens / apis keys etc.... 

URL = 'https://inspirobot.me/api?generate=true'

def check_response(response, log):
    status_code = response.status_code
    log.write(f'Response received with status code {status_code}\n')
    if status_code != 200:
        log.write('Response status code suggests an error\n Exiting program\n')
        sys.exit()
    else:
        log.write('Request successful\n')

with open('log.txt', 'w') as log:
    current_time = datetime.datetime.now().strftime("%m-%b-%y %H:%M:%S")
    log.write(f'Intializing {current_time}\n')
    log.write(f'Making Get request to {URL}\n')
    try:
        response = requests.get(URL)
    except:
        log.write('Request failed\n')
        sys.exit()
    else:
        check_response(response, log)

    log.write('Initializing Slack API client\n')
    client = slack_sdk.WebClient(token=TOKEN)
    img_url = response.text
    attachments = [
        {
            "fallback": "Your daily quote from Inspirobot.",
            "image_url": img_url,
        }
    ]
    log.write('Sending payload to Slack channel\n')
    try:
        response = client.chat_postMessage(
            channel = CHANNEL_ID,
            attachments = attachments
        )
    except SlackApiError as e:
        log.write(f"Error: {e}\n")
    else:
        check_response(response, log)
    log.write('Exiting program\n')
    sys.exit()