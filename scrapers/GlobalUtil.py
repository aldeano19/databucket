"""
Utility accessible to all scripts.
"""

import sys
sys.path.append("..")

import time
import datetime
import math

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

