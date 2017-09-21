"""
Utility accessible to all scripts.
"""
import re
import json
import time
import datetime
import math
import urllib
import os
import sys
# new_modules = "%s/.." % (os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(new_modules)

CONSOLE_LOG_TRUE = True
LOGFILE = ("bjs-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")

# Log levels
LOG_INFO = "INFO"
LOG_WARN = "WARN"
LOG_ERROR = "ERROR"
LOG_DEBUG = "DEBUG"

def extract_src(string):
    regex_str = """(\ssrc=".*?")|(\ssrc='.*?')"""

    print string
    print "="*20
    print regex_str

    match = re.search(regex_str, string.strip())

    return match.group(1)


def get_rest_env():
    DEFAULT_ENVS = {
        "localhost":{
            "domain":"http://localhost",
            "port":"8080",
            "base_path":""
        },
        "t2medium":{
            "domain":"http://13.58.52.4",
            "port":"8088",
            "base_path":"/rest-0.1.0"
        }
    }

    system_in = sys.argv

    if len(system_in) < 2:
        # identifier = "t2medium"
        identifier = "localhost"
    else:
        identifier = system_in[1]

    if identifier in DEFAULT_ENVS:
        message = "Using default env '%s'" % (identifier)
        log(LOGFILE, LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)
        return DEFAULT_ENVS[identifier]

def encode_url_params(dictionary):
    mydata = {}
    for k, v in dictionary.iteritems():
        mydata[k] = unicode(v).encode('utf-8')
    return urllib.urlencode(mydata)

def estimate_remaining_time(total, consumed, start_time):
    """
    Estimates remaining tim given:
        total items at start
        consumed items since started
        start time in milliseconds
    returns estimated time as string in hour:minute:second format 2:4:24
    """

    current_time = time.time() * 1000

    running_time = current_time - start_time

    average_time_per_item = running_time/consumed

    remaining_items = total-consumed

    remaining_estimate_time = remaining_items*average_time_per_item
    seconds=math.floor((remaining_estimate_time/1000)%60)
    minutes=math.floor((remaining_estimate_time/(1000*60))%60)
    hours=math.floor((remaining_estimate_time/(1000*60*60))%24)

    return "%.0f:%.0f:%.0f" % (hours, minutes, seconds)


def calculate_running_time(start_time):
    """
    Calculates how long has the program being running based on start_time
    and the current time
    """
    current_time = time.time() * 1000
    running_time = current_time - start_time

    seconds=math.floor((running_time/1000)%60)
    minutes=math.floor((running_time/(1000*60))%60)
    hours=math.floor((running_time/(1000*60*60))%24)

    return "%.0f:%.0f:%.0f" % (hours, minutes, seconds)

def log(logfile, level, message, console_out=False):
    logdir = os.path.dirname(logfile)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    message = message.encode('ascii','ignore')
    with open(logfile, "a") as f:
        line = "%-15s | %s\n" % (level, message) 
        f.write(line)

    if console_out:
        print message
