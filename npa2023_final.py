#######################################################################################
# Yourname: wasuphon phonsawat
# Your student ID: 65070206
# Your GitHub Repo: https://github.com/AZurui22704/NPA2023-Final.git
#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, and restconf_final.

import json
import requests
import time
from restconf_final import create, delete, enable, disable, status

#######################################################################################
# 2. Assign the Webex hard-coded access token to the variable accessToken.

accessToken = "Bearer M2NhMzYxNGUtMzFkNy00N2E3LTg1OTgtYTIyZTNmMGUxNDNjMjY5N2I4MjgtNTky_P0A1_bc884c7a-820b-497b-8b60-00b4d15ea95d"

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VzL1JPT00vNTFmNTJiMjAtNWQwYi0xMWVmLWE5YTAtNzlkNTQ0ZjRkNGZi"

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authorization
    getHTTPHeader = {"Authorization": accessToken}

    # 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    r = requests.get(
        "https://webexapis.com/v1/messages",  # Webex API endpoint
        params=getParameters,
        headers=getHTTPHeader,
    )
    
    # Verify if the returned HTTP status code is 200/OK
    if r.status_code != 200:
        raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")
    
    # Get the JSON formatted returned data
    json_data = r.json()

    # Check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        continue

    # Store the text of the first message in the array
    message = json_data["items"][0]["text"]
    print("Received message: " + message)

    # Check if the text of the message starts with the magic character "/" followed by your studentID and a command name
    if message.startswith("/66070123"):
        _, command = message.split()  # Split the message to extract the command
        print(command)

        # 5. Complete the logic for each command
        if command == "create":
            responseMessage = create()
        elif command == "delete":
            responseMessage = delete()
        elif command == "enable":
            responseMessage = enable()
        elif command == "disable":
            responseMessage = disable()
        elif command == "status":
            responseMessage = status()
        else:
            responseMessage = "Error: No command or unknown command"
        
        # 6. Complete the code to post the message to the Webex Teams room.
        
        # the Webex Teams HTTP headers, including the Authorization and Content-Type
        postHTTPHeaders = {"Authorization": accessToken, "Content-Type": "application/json"}

        # The Webex Teams POST JSON data
        postData = {"roomId": roomIdToGetMessages, "text": responseMessage}

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",  # Webex API endpoint for posting messages
            data=json.dumps(postData),
            headers=postHTTPHeaders,
        )
        
        if r.status_code != 200:
            raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")
