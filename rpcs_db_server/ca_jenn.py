import sys
import psycopg2
import datetime
import pytz
import time
from math import acos, radians, tan, atan, cos, sin, asin, sqrt
from geopy import distance

# query helper string to filter data in the night
utc = pytz.utc
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
night_start = datetime.time(0, 0, 0)
night_end = datetime.time(7, 0, 0)

curday = 26
curmonth = 4
curdate = datetime.date(2019, curmonth, curday)
patient_id = 2019


def main():
    print("Holy shit this thing ran at " + str(datetime.datetime.now()))
    try:
        # pass
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    else:
        wt_distance_analysis(connection, cursor)
    # fetch_watch_rate(connection, cursor)

    # select_query = "select * from watch_Event"
    # cursor.execute(select_query)
    # watch_analysis(connection, cursor,now)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')


def wt_distance_analysis(connection, cursor):
    select_query = "select location, cast(timestamp AS DATE), patient_id from wt_patient where patient_id = '2019' and extract (day from timestamp) = " + str(curday) + "and extract (month from timestamp) = " + str(curmonth)
    cursor.execute(select_query, (curdate, ))
    wt_patients = cursor.fetchall()
    total_dist = float(0)
    for i in range(len(wt_patients)):
        cur_coor = str2coor(wt_patients[i][0])
        # row = wt_patients[i]
        if i > 0:
            total_dist += distance.distance(cur_coor, pre_coor).km
        pre_coor = cur_coor
        # prev_location = wt_patients[i - 1][0]
        # print(prev_location)
        # total_dist += calculate_distance(row[0], prev_location, row[1], row[2])

    select_query = "select * from ca_incident_summary where date = %s and patient_id = %s"
    cursor.execute(select_query, (curdate, patient_id))
    record = cursor.fetchone()
    if record is None:
        print('insert', patient_id, curdate, total_dist)
        insert_query = "insert into ca_incident_summary (patient_id, date, walk_distance) VALUES (%s, %s, %s)"
        record_to_insert = (patient_id, curdate, total_dist)
        cursor.execute(insert_query, record_to_insert)
    else:
        print('update', patient_id, curdate, total_dist)
        update_query = "update ca_incident_summary set walk_distance = %s where patient_id = %s and date = %s"
        cursor.execute(update_query, (total_dist, patient_id, curdate))
    connection.commit()
    print('Successfully update incident of walk_distance')


def str2coor(location):
    locations = location.split(',')
    lat = float(locations[1])
    lon = float(locations[0])
    return lat, lon


def watch_analysis(connection, cursor, now):
    select_query = "select * from watch_Event where CAST(SUBSTRING(event_description,1,10) AS int) between %s and %s"
    cursor.execute(select_query, (int(now) - 43200, now))
    watch_events = cursor.fetchall()
    for row in watch_events:
        if row[2] == 'string':
            continue
        if row[3] == "fall":
            update_num_of_falls(connection, cursor, row[2])


def wt_analysis(connection, cursor):
    trigger_query = "CREATE TRIGGER IfWandering UPDATE ON ca_wandering FOR EACH ROW WHEN (OLD.isWandering IS DISTINCT FROM NEW.isWandering) SELCET isWandering FROM ca_wandering"
    query = "select isWandering from ca_wandering"
    cursor.execute(query)
    wt_wandering = cursor.fetchall()
    print(wt_wandering)


def fetch_watch_rate(connection, cursor):
    # event_id = 1, event_category = "92.000,100.000"
    select_query = "select event_category from watch_event where event_id = 1"
    cursor.execute(select_query)
    record = cursor.fetchall()
    newest_record = record[-1].split(',')
    update_query = "update ct_incident  set pulse_rate  = %s, respiratory = %s where pulse_rate = None and reapiratory = None"
    # select_query = "select pulse_rate, respiratory_rate where pulse_rate = None and reapiratory_rate = None"
    cursor.execute(update_query, (newest_record[0], newest_record[1]))
    print('Successfully update the pulse and respiratory rate!')


def lat_lng_distance(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.140
    rb = 6356.755
    flatten = (ra - rb) / ra
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    print("calculate distance")
    return distance


def calculate_distance(location, prev_location, wt_date, wt_patient_id):
    if not location or not wt_date or not wt_patient_id or location == 'string':
        return 0

    if not prev_location or prev_location == 'string':
        return 0
    # print (location, prev_location)
    location = location.split(',')
    lat1 = float(location[0])
    lon1 = float(location[1])

    prev_location = prev_location.split(',')
    lat2 = float(prev_location[0])
    lon2 = float(prev_location[1])
    # print (lat1, lon1, lat2, lon2)
    distance = lat_lng_distance(lat1, lon1, lat2, lon2)
    return distance


def update_num_of_falls(connection, cursor, timestamp):
    sql_query = "select * from ca_incident_summary where date = %s"
    timestamp = datetime.datetime.fromtimestamp(float(timestamp[:10]))
    curdate = timestamp.date()
    # print (curdate)
    cursor.execute(sql_query, (curdate,))
    record = cursor.fetchone()
    if record:
        # print ("update num_falls")
        # print (record)
        # update_query = "update ca_incident_summary set num_falls = 0 where patient_id = 1 and date = %s"
        # cursor.execute(update_query, (curdate,))
        update_query = "update ca_incident_summary set num_falls = num_falls + 1 where patient_id = 1 and date = %s"
        cursor.execute(update_query, (curdate,))
    else:
        # print ("insert num_falls")
        insert_query = "insert into ca_incident_summary (patient_id, date, num_falls) VALUES (%s, %s, %s)"
        record_to_insert = (1, curdate, 1)
        cursor.execute(insert_query, record_to_insert)
    connection.commit()
    print("Successfully update ca incident summary of num_falls")


if __name__ == "__main__":
    main()
    sys.exit(0)
