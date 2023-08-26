import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pprint


"""
TODO Incoming webhooks
- Save the incoming messages and store in list[list[str]]. Embed the
messages and find average embedding
"""

# Docs https://slack.dev/python-slack-sdk/api-docs/slack_sdk/

pp = pprint.PrettyPrinter(indent=2)

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

try:
    response = client.chat_postMessage(channel='#random', text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")

# You probably want to use a database to store any user information ;)
users_store = {}


# Put users into the dict
def save_users(users_array):
    for user in users_array:
        # Key user info on their unique user ID
        user_id = user["id"]
        # Store the entire user object (you may not need all of the info)
        users_store[user_id] = user
    pp.pprint(users_store)

try:
    # Call the users.list method using the WebClient
    # users.list requires the users:read scope
    result = client.users_list()
    save_users(result["members"])

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
