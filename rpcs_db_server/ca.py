import sys
import psycopg2
import datetime
import pytz

# query helper string to filter data in the night
utc = pytz.utc
filter_night = "extract (hour from timestamp) >= 0 and extract (hour from timestamp) <= 7"
def main():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
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
                        # insert bathroom entry into table
                        print("New entry at: ", hs_br_entry_ts)
                    else:
                        hs_br_entry_ts = row[4]
                        hs_br_rfid = True
                if row[3] == 'motion' and 'MOTION_STARTED' in row[5]:
                    if hs_br_rfid and (row[4] - hs_br_entey_ts).total_seconds() < 200:
                        hs_br_flag = True
                        # insert bathroom entry into table
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
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')

if __name__ == "__main__":
    main()
    sys.exit(0)
