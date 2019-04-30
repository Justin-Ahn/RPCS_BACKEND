import math
import sys
import psycopg2
import datetime
import pytz
import time

# query helper string to filter data in the night
utc = pytz.utc
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
night_start = datetime.time(0, 0, 0)
night_end = datetime.time(7, 0, 0)


def main(now):
    try:
        # pass
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
        # wt_analysis(connection, cursor)
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    else:
        # wt_distance_analysis(connection, cursor)
        fetch_watch_rate(connection, cursor)

        # select_query = "select * from watch_Event"
        # cursor.execute(select_query)
        # watch_analysis(connection, cursor,now)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')


def wt_distance_analysis(connection, cursor):
    select_query = "select location, cast(timestamp AS DATE), patient_id from wt_patient"
    cursor.execute(select_query)
    wt_patients = cursor.fetchall()
    for row in wt_patients:
        # print (row)
        calculate_distance(connection, cursor, row[0], row[1], row[2])


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


def calculate_distance(connection, cursor, location, wt_date, wt_patient_id):
    if not location or not wt_date or not wt_patient_id or location == 'string':
        return
    location = location.split(',')
    latitude = float(location[0])
    longtitude = float(location[1])
    distance = math.sqrt(latitude ** 2 + longtitude ** 2)
    select_query = "select * from ca_incident_summary where date = %s and patient_id = %s"
    cursor.execute(select_query, (wt_date, wt_patient_id))
    record = cursor.fetchone()
    if record is None:
        print('insert', wt_patient_id, wt_date, distance)
        insert_query = "insert into ca_incident_summary (patient_id, date, walk_distance) VALUES (%s, %s, %s)"
        record_to_insert = (wt_patient_id, wt_date, distance)
        cursor.execute(insert_query, record_to_insert)
    else:
        print('update', wt_patient_id, wt_date, distance)
        update_query = "update ca_incident_summary set walk_distance = walk_distance + %s where patient_id = %s and date = %s"
        cursor.execute(update_query, (distance, wt_patient_id, wt_date))
    connection.commit()
    print('Successfully update incident of walk_distance')
    # print('Successfully update incident summary-hallucinations')


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
    # connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
    # cursor = connection.cursor()
    while (1):
        now = int(time.time())
        main(now)
        time.sleep(5)
    # connection.close()
    # cursor.close()
    # sys.exit(0)
