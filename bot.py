"""Main script

This script requires python-twitter.
"""

import datetime
import itertools
import logging
import sys
import time

logging.basicConfig(format = '%(asctime)s %(levelname)s: %(message)s',handlers=[logging.FileHandler('botlog.log'), logging.StreamHandler(sys.stdout)], level=logging.INFO)
from login import api
from twitter.error import TwitterError

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
    tweets.append(cur)
    return tweets


def calculate_dates(numbers):
    dates = []
    for i in numbers:
        dates.append((i, (datetime.datetime.utcnow() - datetime.timedelta(days=i)).strftime("%m/%d/%Y")))
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
        try:
            _main()
        except TwitterError:
            pass
        m, d, y = [int(x) for x in datetime.datetime.utcnow().strftime('%D').split('/')]
        s = (((datetime.datetime(y, m, d)) + datetime.timedelta(days=1)) - datetime.datetime.utcnow()).seconds
        s += 1
        logging.info('Sleeping until %s, will wake up in %s' % (s, datetime.datetime.utcnow()+datetime.timedelta(seconds=s)))
        time.sleep(s)

if __name__ == '__main__':
    main()