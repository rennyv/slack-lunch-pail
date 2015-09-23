from pyslack import SlackClient
import yaml
from datetime import datetime, timedelta
import time
import random

username = 'lunchpail'
channel = '#general'
wait_time_in_minutes = 10

def main():
    today = datetime.today()
    if is_a_workday(today):
        # we're awake!
        client = SlackClient(get_api_key())

        announce_lunch(client)
        suggest_places(client)
        wait_for_responses(client)
        say_goodbye(client)

def announce_lunch(client):
    print 'Announcing lunch.'
    send_message(client, "It's lunchtime, motherfuckers")

def suggest_places(client):
    possible_places = ['Mucho Burrito'] * 2 + ['the University Food Court'] * 20 + ['the Mall'] * 1 + ['Five Guys'] * 3 + ['train station Vietnamese'] * 1 + ['Harveys'] * 1 + ["Wendy's"] * 3
    send_message(client, "maybe today you motherfuckers should go to " + random.choice(possible_places))

def wait_for_responses(client):
    start_time = datetime.now()
    last_checked = start_time

    print 'Waiting for responses.'
    # wait 10 minutes for orders and stuff
    while (last_checked - start_time).total_seconds() < wait_time_in_minutes * 60:

        # TODO: Get messages since last time
        # TODO: Handle those messages

        last_checked = datetime.now()
        time.sleep(2)

    print 'Done with handling responses', wait_time_in_minutes, 'minutes has elapsed.'

def say_goodbye(client):
    send_message(client, "Enjoy your lunch, motherfuckers")
    print 'Shutting down'

def send_message(client, msg):
    icon_url = "http://i.imgur.com/pP4x0tO.png"
    client.chat_post_message(channel, msg, username=username, icon_url=icon_url)

def get_api_key():
    with open('secrets.yml') as stream:
        data = yaml.load(stream)
        return data["api_key"]

def is_a_workday(d):
    return d.weekday() < 5

if __name__ == '__main__': main()
