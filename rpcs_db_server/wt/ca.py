"""
Author: Xiaoyu
QAQ

This file will detect and update wandering incident

input table:
output table: ca_incident_summary

"""
import psycopg2
import datetime as dt
from pytz import timezone
import time
import json

est = timezone('US/Eastern')
cd_length = dt.timedelta(minutes=5)

# query helper string to filter data in the night
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
night_start = dt.time(0, 0, 0)
night_end = dt.time(7, 0, 0)


# Detect and update wandering incident
# return boolean: whether or not to send alert to caregiver
def update_wandering(data):
    with open('var_state.json', 'r+') as f:
        json_data = json.load(f)
        write_json(f, json_data)
    return False


def write_json(file, json_data):
    file.seek(0)
    json.dump(json_data, file, indent=4)
    file.truncate()
