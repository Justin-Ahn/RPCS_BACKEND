import psycopg2
import sys
import datetime
import pytz
import time
import math

# query helper string to filter data in the night
utc = pytz.utc
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
night_start = datetime.time(0, 0, 0)
night_end = datetime.time(7, 0, 0)

def main():
    print("Holy shit this thing ran at " + str(datetime.datetime.now()))
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
        #wt_analysis(connection, cursor)
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    else:
        ct_analysis(connection, cursor)
        hs_analysis(connection, cursor)
        watch_analysis(connection, cursor)
        wt_distance_analysis(connection, cursor)
        stove(connection, cursor)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')

def stove(connection, cursor):
    select_query = "select * from hs_events limit 100 offset 100"
    cursor.execute(select_query)
    hs_events_data = cursor.fetchall()
    hs_events(hs_events_data)

def hs_events(data):
    data_type = []    #data or handshake
    message = []
    value = []
    time_prime = []
    time_hour = []

#get data about stove
    for i in range(len(data)):
        if data[i][2] == 'grid_eye' and data[i][0] == 'data' :
            index_me_left = data[i][4].index(":")
            if data[i][4][index_me_left + 3] == "S":
                data_type.append(data[i][0])
                index_left = data[i][4].index("[")
                index_right = data[i][4].index("]")
                index_me_right = data[i][4].index(",")
                message.append(data[i][4][index_me_left + 3: index_me_right-1])
                value.append(data[i][4][index_left + 1 : index_right].split(','))
                time_prime.append(data[i][3])    
#get data about motion
    time_motion = []
    type_motion = []
    for i in range(len(data)):
        if data[i][2] == 'pir' and data[i][0] == 'data':
            index_pir_left = data[i][4].index("m")
            type_motion.append(data[i][4][index_pir_left+11])
            time_motion.append(data[i][3])
#    print(type_motion)

#change string to float for stove temperature.
    for i in range(len(value)):
        for j in range(len(value[0])):
            value[i][j] = float(value[i][j])
#calculate average stove temperature
    average_value = [0]*len(value)
    for i in range(len(value)):
        average_value[i]= float(sum(value[i]) / 64)
        
        
#set time decision boundary
    timestr_low = "time2019-04-21 18:00"
    time_low = time.strptime(timestr_low,"time%Y-%m-%d %H:%M")
    time_lower = datetime.datetime(*time_low[:6])
    time_lower = time_lower.replace(tzinfo = pytz.timezone('UTC'))
    
    timestr_high = "time2019-04-22 06:00"
    time_high = time.strptime(timestr_high,"time%Y-%m-%d %H:%M")
    time_higher = datetime.datetime(*time_high[:6])
    time_higher = time_higher.replace(tzinfo = pytz.timezone('UTC'))

    timestr_sec = "time2019-04-22 18:00"
    time_sec = time.strptime(timestr_sec,"time%Y-%m-%d %H:%M")
    time_secer = datetime.datetime(*time_sec[:6])
    time_secer = time_secer.replace(tzinfo = pytz.timezone('UTC'))
    
    
#analyze night
    for i in range(len(time_prime)):
        if time_prime[i] < time_higher and time_prime[i] > time_lower and average_value[i] > 30:
            print("danger in night")
            print(time_prime[i])
            break
   
#analyze day
    for i in range(len(time_prime)):
        if time_prime[i] > time_higher and time_prime[i] < time_secer and average_value[i] > 30:
            for j in range(len(time_motion)):
                if time_motion[j] < time_prime[i] and time_motion[j+1]>time_prime[i]:
                    if type_motion[j] == 'U' and type_motion[j+1] == 'M':
                        print('danger in day')
                        break
#analyze night
 #   for i in range(len(time_prime)):
 #       if check_night(time_prime[i]) is True:
 #           if average_value[i] > 30:
 #               print("danger in night")
 #               print(time_prime[i])
 #               break
#analyze day
 #   for i in range(len(time_prime)):
 #       if check_night(time_prime[i]) is False:
 #           if average_value[i] > 30:
 #               for j in range(len(time_motion)):
 #                   if time_motion[j] < time_prime[i] and time_motion[j+1]>time_prime[i]:
 #                       if type_motion[j] == 'U' and type_motion[j+1] == 'M':
 #                           print('danger in day')
 #                           break



def ct_analysis(connection, cursor):
    select_query = "select * from ct_incident"
    cursor.execute(select_query)
    print('Selecting rows from ct_incident table using cursor.fetchall')
    ct_incidents = cursor.fetchall()
    for row in ct_incidents:
        update_incident(connection, cursor, row[7], row[3])

def watch_analysis(connection, cursor) :
    select_query = "select * from watch_Event"
    cursor.execute(select_query)
    watch_events = cursor.fetchall()
    for row in watch_events :
        # row[3] is event_category
        if row[3] == "fall" :
            update_num_of_falls(connection, cursor, row[2])

def wt_analysis(connection, cursor):
    trigger_query = "CREATE TRIGGER IfWandering UPDATE ON ca_wandering FOR EACH ROW WHEN (OLD.isWandering IS DISTINCT FROM NEW.isWandering) SELCET isWandering FROM ca_wandering"
    query = "select isWandering from ca_wandering"
    cursor.execute(query)
    wt_wandering = cursor.fetchall()
    print(wt_wandering)


def wt_distance_analysis(connection, cursor) :
    select_query = "select location, timestamp, patient_id from wt_patient where timestamp between %s and %s"
    cursor.execute(select_query,(datetime.datetime.today()-datetime.timedelta(days=1),datetime.datetime.today()))
    wt_patients = cursor.fetchall()
    for row in wt_patients :
        #print (row)
        calculate_distance(connection, cursor, row[0],row[1], row[2])
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
                    #print("New entry at: ", hs_br_entry_ts)
                else:
                    hs_br_entry_ts = row[4]
                    hs_br_rfid = True
            if row[3] == 'motion' and 'MOTION_STARTED' in row[5]:
                if hs_br_rfid and (row[4] - hs_br_entey_ts).total_seconds() < 200:
                    hs_br_flag = True
                    # if at night, add bathroom entry into sleep_trend table
                    if check_night(hs_br_entry_ts):
                        update_night_br_usage(connection, cursor, hs_br_entry_ts)
                    #print("New entry at: ", hs_br_entry_ts)
                else:
                    hs_br_entry_ts = row[4]
                    hs_br_motn = True
        else:
            if row[3] == 'rfid' and 'UNBROKEN' not in row[5]:
                return
                # insert bathroom exit into table
                #print("New exit at: ", row[4] ,#print('ID = ', row[0])#print('event_type = ', row[1])#print('sensor_id = ', row[2])#print('sensor_type = ', row[3])#print('timestamp = ', row[4])#print('data = ', row[5], '\n')

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

def calculate_distance(connection, cursor, location, wt_date, wt_patient_id):
    if not location or not wt_date or not wt_patient_id or location == 'string':
        return
    wt_date = wt_date.date()
    location = location.split(',')
    latitude = float(location[0])
    longtitude = float(location[1])
    distance = math.sqrt(latitude**2 + longtitude**2)
    select_query = "select * from ca_incident_summary where date = %s and patient_id = %s"
    cursor.execute(select_query,(wt_date, wt_patient_id))
    record = cursor.fetchone()
    if record is None :
        print ('insert',wt_patient_id, wt_date, distance)
        insert_query = "insert into ca_incident_summary (patient_id, date, walk_distance) VALUES (%s, %s, %s)"
        record_to_insert = (wt_patient_id, wt_date, distance)
        cursor.execute(insert_query, record_to_insert)
    else :
        #print ('update', wt_patient_id, wt_date, distance)
        update_query = "update ca_incident_summary set walk_distance = walk_distance + %s where patient_id = %s and date = %s"
        cursor.execute(update_query, (distance, wt_patient_id, wt_date))
    connection.commit()
    print('Successfully update incident of walk_distance')
def update_num_of_falls(connection, cursor, timestamp) :
    sql_query = "select * from ca_incident_summary where date = %s"
    timestamp = datetime.datetime.fromtimestamp(float(timestamp[:10]))
    curdate = timestamp.date()
    cursor.execute(sql_query, (curdate,))
    record = cursor.fetchone()
    if record :
        print ("update num_falls")
        #cursor.execute(update_query, (curdate,))
        update_query = "update ca_incident_summary set num_falls = num_falls + 1 where patient_id = 1 and date = %s"
        cursor.execute(update_query,(curdate,))
    else:
        print ("insert num_falls")
        insert_query = "insert into ca_incident_summary (patient_id, date, num_falls) VALUES (%s, %s, %s)"
        record_to_insert = (1, curdate, 1) 
        cursor.execute(insert_query, record_to_insert)
    connection.commit()
    print("Successfully update ca incident summary of num_falls")
    

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
