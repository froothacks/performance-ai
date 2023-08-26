

# from anthropic.client import Client
import slack
import re
import os

# client = anthropic.Client(api_key='YOUR_API_KEY')
# slack_client = slack.WebClient(token='YOUR_SLACK_TOKEN')

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from anthropic import Anthropic

ant = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
# slack_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
slack_client_1 = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
slack_client_2 = WebClient(token=os.environ['SLACK_BOT_TOKEN_2'])

users = ['john', 'mary', 'peter']
user_ids = ['D05QD7BA5UY', 'D05PPD6L41Z', 'D05PPG1816E']

def get_user_id(username):
  if username == 'john':
    return user_ids[0]
  elif username == 'mary':  
    return user_ids[1]
  elif username == 'peter':
    return user_ids[2]
  
  return user_ids[0] # default

def get_username(message):

  users = ['john', 'mary', 'peter']

  for user in users:
    pattern = rf'^{user}:'
    match = re.search(pattern, message)
    
    if match:
      return user

  # If no match, try to extract username
  pattern = r'^([a-zA-Z]*):'
  match = re.search(pattern, message)

  if match:
    return match.group(1)

def generate_thread():
  prompt = "\n\nHuman: Generate a simulated Slack conversation between coworkers - it can be a debate, technical discussion, idea discussion, argument, kudos thread, design discussion, problem solving, mentorship, or anything else. Switch users appropriately.\n\nAssistant:"

  response = ant.completions.create(
    model="claude-2",
    prompt=prompt,
    max_tokens_to_sample=1000,
    # stop=["Human:", "Assistant:"]
  )
  print(response.completion) 
  return response.completion

global_counter = 0

def post_slack_message(client, username, text, thread, alternate):
  global global_counter
  user_id = get_user_id(username)
  print("TEXT text", text)
  print("userr", username)
  if text == "":
    return
  print("THREAD_TS INSIDE", thread)
  print("ALTENRATE HEREEE", alternate)

  global_counter += 1
  if global_counter % 2 == 0:
    use_client = slack_client_2
  else:
    use_client = client
  response = use_client.chat_postMessage(
    channel='general',
    text=text,
    thread_ts=thread, 
    # as_user=False,
    # username=username,
    username="advait",
    icon_url="https://headshots-inc.com/wp-content/uploads/2021/02/FINAL-Blog-Images.jpg",
    # icon_url="https://images.unsplash.com/photo-1552374196-c4e7ffc6e126?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d2hpdGUlMjBtYW58ZW58MHx8MHx8fDA%3D&w=1000&q=80",
    # icon_url="https://ca.slack-edge.com/T05P8LW21K9-U05PRUP0Y68-7cdf473ed182-512",
    icon_emoji=":robot_face:",
    # username=username,
    # user=user_id
  )

  thread_ts = response['ts']

  return thread_ts


threads = []

for i in range(10):
  
  thread = generate_thread()
  threads.append(thread)

  thread_ts = None

  messages = thread.split("\n")
  print("MESSAGE SPLIT")
  print(messages)

  thread_ts = post_slack_message(
    slack_client_1, 
    "bot", 
    thread.split("\n")[0], # First msg
    None,
    0
  )
  print("thread_ts 1", thread_ts)

  messages = thread.split("\n")[1:] # Remaining msgs

  
  for incre, message in enumerate(messages):
    
    username = get_username(message) 
    print("INCRE", incre)
    post_slack_message(
      slack_client_1,
      username, 
      message,
      thread_ts, # Pass thread_ts here
      incre + 1
    )

print("Posted Slack threads impersonating users")
