"""Main script

If you are trying to replicate, login.py should look like this:
```
import twitter
api = twitter.Api(consumer_key="nxfWd3hAOea7SHIkHzjMYxRLC ",
                  consumer_secret="e0z64U3DU8WiHDDz9dZHrTguMeoS5bwU1B0GxysPIcp46UzJKg ",
                  access_token_key="1090760044503801859-GNDuUrceIIzlwvcRc0gVVAxM5Jquhc",
                  access_token_secret="f6Jg9Lu2hQw7tK6Dil8vF4iCxgQ9KVr7DoTIJEn7bfUa2",
                  sleep_on_rate_limit=True)
```

This script requires python-twitter.
"""

import datetime
import itertools
import logging
import sys
import time

logging.basicConfig(format = '%(asctime)s %(levelname)s: %(message)s',handlers=[logging.FileHandler('botlog.log'), logging.StreamHandler(sys.stdout)], level=logging.INFO)
from login import api

def tweetsnipper(sentences):
    """Snips sentences into tweets of 280 characters or less."""
    tweets = []
    cur = c = ""
    for i in sentences:
        c += i + '\n'
        if len(c)<280:
            cur = c
        else:
            tweets.append(cur)
            cur = c = i + '\n'
    return tweets


def calculate_dates(numbers):
    dates = []
    for i in numbers:
        dates.append((i,(datetime.datetime.utcnow()-datetime.timedelta(days = i)).strftime("%D")))
    return dates

def inttostr(dates, *args):
    sentences = list(args)
    for a,b in dates:
        sentences.append("%s is %s days ago." % (b,a))
    return sentences

def _main():
    intro = "Here are the special dates for " + datetime.datetime.utcnow().strftime("%A, %B %d, %Y") + "."
    nums = [69,420,666]
    nums.extend([eval(str(a)+str(b)) for a,b in itertools.permutations([69,420,666], 2)])
    nums.extend([eval(str(a)*2) for a in [69,420,666]])
    nums.extend([6666,66666])
    nums = list(set(nums))
    nums.sort()
    tweets = tweetsnipper(inttostr(calculate_dates(nums),intro))
    prev = None
    for i in tweets:
        logging.info('Tweeting \n%s' % i)
        if prev is None:
            prev = api.PostUpdate(i).id
        else:
            prev = api.PostUpdate(i, in_reply_to_status_id=prev).id
    logging.info("Tweeted all")

def main():
    while True:
        _main()
        m,d,y = datetime.datetime.utcnow().strftime('%D').split('/')
        s = (datetime.datetime(y,m,d+1)-datetime.datetime.utcnow()).seconds
        logging.info('Sleeping until %s, will wake up in %s' % (s, datetime.datetime.utcnow()+datetime.timedelta(seconds=s)))
        time.sleep(s+60)

if __name__ == '__main__':
    main()