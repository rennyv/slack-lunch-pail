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
        # sleep until 11:30 AM
        t = datetime.now(time_zone)
        future = datetime(t.year, t.month, t.day, waking_hour, waking_minutes, tzinfo=time_zone)
        if t.hour >= waking_hour:
            # wait until tomorrow!
            # admittedly not a perfect solution, because if we fire
            # this up at 11:20 it will wait until 11:30 the *next* day.
            # TODO: incorporate waking_minutes
            future += timedelta(days = 1)


        seconds_to_wait = (future - t).total_seconds()
        print "Sleeping for", seconds_to_wait, "seconds until lunch."

        time.sleep(seconds_to_wait)

        # we're awake!
        client = SlackClient(api_key)
        client.chat_post_message(channel, message, username=username)


if __name__ == '__main__': main()
