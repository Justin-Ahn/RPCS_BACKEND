import sys
import psycopg2
import datetime
import pytz

# query helper string to filter data in the night
utc = pytz.utc
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
night_start = datetime.time(0, 0, 0)
night_end = datetime.time(7, 0, 0)

def main():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    else:
        ct_analysis(connection, cursor)
        hs_analysis(connection, cursor)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')

def ct_analysis(connection, cursor):
    select_query = "select * from ct_incident"
    cursor.execute(select_query)
    print('Selecting rows from ct_incident table using cursor.fetchall')
    ct_incidents = cursor.fetchall()
    for row in ct_incidents:
        update_incident(connection, cursor, row[7], row[3])

def hs_analysis(connection, cursor):
    # home sensor: determine room entry
    hs_br_flag = False
    hs_br_rfid = False
    hs_br_motn = False
    hs_br_entry_ts = datetime.datetime(2005, 7, 14, 12, 30, tzinfo=utc)    

    hs_kt_flag = False
    hs_kt_rfid = False
    hs_kt_motn = False
    hs_kt_entry_ts = datetime.datetime(2005, 7, 14, 12, 30)
    postgreSQL_select_Query = "select * from hs_events where " + filter_night
        
    cursor.execute(postgreSQL_select_Query)
    print('Selecting rows from hs table using cursor.fetchall')
    hs_events = cursor.fetchall()
    for row in hs_events:
        if not hs_br_flag:
            if row[3] == 'rfid' and 'BROKEN' in row[5]:
                if hs_br_motn and (row[4] - hs_br_entry_ts).total_seconds() < 200:
                    hs_br_flag = True
                    # if at night, add bathroom entry into sleep_trend table
                    if check_night(hs_br_entry_ts):
                        update_night_br_usage(connection, cursor, hs_br_entry_ts)
                    print("New entry at: ", hs_br_entry_ts)
                else:
                    hs_br_entry_ts = row[4]
                    hs_br_rfid = True
            if row[3] == 'motion' and 'MOTION_STARTED' in row[5]:
                if hs_br_rfid and (row[4] - hs_br_entey_ts).total_seconds() < 200:
                    hs_br_flag = True
                    # if at night, add bathroom entry into sleep_trend table
                    if check_night(hs_br_entry_ts):
                        update_night_br_usage(connection, cursor, hs_br_entry_ts)
                    print("New entry at: ", hs_br_entry_ts)
                else:
                    hs_br_entry_ts = row[4]
                    hs_br_motn = True
        else:
            if row[3] == 'rfid' and 'UNBROKEN' not in row[5]:
                # insert bathroom exit into table
                print("New exit at: ", row[4])
                        
        print('ID = ', row[0])
        print('event_type = ', row[1])
        print('sensor_id = ', row[2])
        print('sensor_type = ', row[3])
        print('timestamp = ', row[4])
        print('data = ', row[5])
        print('event_id = ', row[6], '\n')

def update_incident(connection, cursor, incident_type, timestamp):
    #TODO: only hallucination in incident summary?
    if incident_type != 'hallucination':
        return
    select_query = "select * from ca_incident_summary where date = %s"
    curdate = timestamp.date()
    cursor.execute(select_query, (curdate,))
    record = cursor.fetchone()
    if record is None:
        insert_query = "insert into ca_incident_summary (patient_id, date, num_hallucinations) VALUES (%s, %s, %s)"
        record_to_insert = (1, curdate, 1)
        cursor.execute(insert_query, record_to_insert)
    else:
        update_query = "update ca_incident_summary set num_hallucinations = num_hallucinations + 1 where patient_id = 1 and date = %s"
        cursor.execute(update_query, (curdate,))
    connection.commit()
    print('Successfully update incident summary-hallucinations')


def update_night_br_usage(connection, cursor, timestamp):
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

def check_night(timestamp):
    return night_start <= timestamp.time() <= night_end

def get_date(timestamp):
    return timestamp.date()

if __name__ == "__main__":
    main()
    sys.exit(0)
