from pyslack import SlackClient
import yaml
from datetime import datetime, timedelta
import time
import pytz

username = 'lunchpail'
channel = '#general'
message = "it's lunchtime, motherfuckers"

def get_api_key():
    with open('secrets.yml') as stream:
        data = yaml.load(stream)
        return data["api_key"]

def main():
    api_key = get_api_key()

    waking_hour = 11
    waking_minutes = 30

    time_zone = pytz.timezone('MST')

    while True:
        # sleep until 11:30
        # -1 is a DST hack... TODO: figure out how to use pytz with DST
        # TODO: figure out if the target date of 'next lunch' is in DST
        seconds_to_wait = get_seconds_to_next_lunchtime(waking_hour - 1, waking_minutes, time_zone)

        print "Sleeping for", seconds_to_wait, "seconds until lunch."

        time.sleep(seconds_to_wait)

        # we're awake!
        client = SlackClient(api_key)
        client.chat_post_message(channel, message, username=username)

def get_seconds_to_next_lunchtime(lunch_hour, lunch_minute, time_zone):
    # TODO: exclude weekends
    t = datetime.now(time_zone)
    future = datetime(t.year, t.month, t.day, lunch_hour, lunch_minute, tzinfo = time_zone)

    minutes_elapsed = t.hour * 60 + t.minute
    if minutes_elapsed >= (lunch_hour * 60 + lunch_minutes):
        # we're looking for TOMORROW's lunch.
        future += timedelta(days = 1)

    seconds_to_wait = (future - t).total_seconds()
    return seconds_to_wait

if __name__ == '__main__': main()
