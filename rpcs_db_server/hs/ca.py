"""
Author: Xiaoyu
QAQ

This file will detect and update overnight bathroom usage

input table: hs_events (sensor_type=bathroom rfid, bathroom pir)
output table: ca_sleep_trend (num_go_to_bathroom)

"""
import psycopg2
import datetime as dt
from pytz import timezone
import time
import json
import sys

est = timezone('US/Eastern')
cd_length = dt.timedelta(minutes=3)

# query helper string to filter data in the night
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
night_start = dt.time(0, 0, 0)
night_end = dt.time(7, 0, 0)

br_gateway_id = 'c26e4e88-2ecb-42ff-8482-4af80307a485'
br_motion_id = 'c76c5d12-6647-11e9-a923-1681be663d3e'

# Download the helper library from https://www.twilio.com/docs/python/install
import twilio
from twilio.rest import Client

account_sid = 'ACcb394859c733f5274639779eab2cb0a4'
auth_token = '6470e99bc9d9373f286f89e647db5ec7'
client = Client(account_sid, auth_token)
est = timezone('US/Eastern')


# Update overnight bathroom usage
# return boolean: whether or not to send alert to caregiver
def update_br_usage(data):
    print("in update_br_usage")
    sensor_id = str(data[1])
    if sensor_id != br_motion_id and sensor_id != br_gateway_id:
        print("not pid or rfid for the bathroom")
        return False
    with open('hs/var_state.json', 'r+') as f:
        json_data = json.load(f)
        cd_ts = str2datetime(json_data['cd_ts'])
        cur_ts = data[3]
        # first check if we are in 'cool down' mode
        if cd_now(cd_ts, cur_ts):
            print("cooling down")
            print("cool down timestamp: " + str(cd_ts))
            print("current timestamp: " + str(cur_ts))
            return False
        rfid_ts = str2datetime(json_data['br_rfid_ts'])

        if json_data['br_rfid']:  # if gateway sensor already triggered
            print("here got rfid = true, probably check entry")
            if sensor_id == br_motion_id and "MOTION DETECTED" in data[4]:  # check whether motion is detected
                if (cur_ts - rfid_ts).total_seconds() < 20:
                    print("new entry!")
                    update_in_db(cur_ts)
                    json_data['br_rfid'] = False
                    json_data['cd_ts'] = str(cur_ts + cd_length)
                    print("cd_ts: " + json_data['cd_ts'])
                    write_json(f, json_data)
                    return True
            elif sensor_id == br_gateway_id:  # if gateway sensor is triggered again, update its timestamp
                print("update rfid timestamp")
                json_data['br_rfid_ts'] = str(cur_ts)
                write_json(f, json_data)
        else:  # if gateway sensor is not triggered (patient not in bathroom)
            if sensor_id == br_gateway_id:
                print("set rfid as true")
                json_data['br_rfid'] = True
                json_data['br_rfid_ts'] = str(cur_ts)
                write_json(f, json_data)
    return False


def str2datetime(string):
    return est.localize(dt.datetime.strptime(string[0:-6], '%Y-%m-%d %H:%M:%S.%f'))


def write_json(file, json_data):
    file.seek(0)
    json.dump(json_data, file, indent=4)
    file.truncate()


def update_in_db(timestamp):
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    else:
        select_query = "select * from ca_sleep_trend where date = %s"
        curdate = timestamp.date()
        cursor.execute(select_query, (curdate,))
        record = cursor.fetchone()
        if record is None:
            insert_query = "insert into ca_sleep_trend (patient_id, date, num_go_to_bathroom) VALUES (%s, %s, %s)"
            record_to_insert = (1, curdate, 1)
            cursor.execute(insert_query, record_to_insert)
        else:
            update_query = "update ca_sleep_trend set num_go_to_bathroom = num_go_to_bathroom + 1 where patient_id = 1 and date = %s"
            cursor.execute(update_query, (curdate,))
        connection.commit()
        print('Successfully update night bathroom usage')
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')


# are we cooling down now?
def cd_now(cd_ts, cur_ts):
    return cur_ts < cd_ts


def check_night(timestamp):
    return night_start <= timestamp.time() <= night_end


def get_date(timestamp):
    return timestamp.date()
