"""
Author: Lynne Chang

This file analyzes data sent from pillow sensor and pressure mat sensor,
and updates #wake up & #go out of bed overnight in the database.

input table: hs_events
output table: ca_sleep_trend

"""
import psycopg2
import sys
import datetime
import pytz


def main():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
        # wt_analysis(connection, cursor)
        mat, pillow = bed_analysis(connection, cursor)
        print(datetime.date(2019, 4, 28))
        if mat > 0:
            print(type(datetime.date(2019, 4, 28)))
            update_num_get_out_of_bed(connection, cursor)
        if pillow > 0:
            update_num_wake_up(connection, cursor)
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL', error)
    else:
        bed_analysis(connection, cursor)
        print('success')
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')


def bed_analysis(connection, cursor):
    filter_night = "extract (hour from timestamp) >= 0  and extract (hour from timestamp) <= 23"
    # query_night = "select * from hs_events where " + filter_night
    query_night = "select * from hs_events where sensor_type='pillow' or sensor_type='pressure_mat'"
    cursor.execute(query_night)
    data = cursor.fetchall()
    off_bed = 0
    off_pillow = 0
    mat_flag = False
    pillow_flag = True
    mat_start_date = datetime.date(2019, 4, 28)
    pillow_start_date = datetime.date(2019, 4, 28)
    mat_record = []
    pillow_record = []
    last_mat_time = datetime.datetime(2019, 4, 28, 12, 58, 49, 342380).replace(tzinfo=pytz.timezone('US/Eastern'))
    last_pillow_time = datetime.datetime(2019, 4, 28, 14, 6, 37, 342380).replace(tzinfo=pytz.timezone('US/Eastern'))

    for i in range(len(data)):
        sensor_time = data[i][3]
        # analyze mat pressure sensor
        if data[i][2] == 'pressure_mat' and data[i][0] == 'data':
            mat_search_date = data[i][3].date()
            if mat_search_date == mat_start_date:
                if mat_flag:
                    if "FEET_DETECTED" in data[i][4] and (sensor_time - last_mat_time).total_seconds() <= 10:
                        last_mat_time = sensor_time
                else:
                    if "FEET_DETECTED" in data[i][4]:
                        off_bed += 1
                        mat_flag = True
                        last_mat_time = sensor_time
            else:
                mat_record.append(off_bed)
                mat_start_date = mat_search_date
                last_mat_time = sensor_time
                off_bed = 1
        if (sensor_time - last_mat_time).total_seconds() > 10:
            mat_flag = False
        # analyze pillow pressure sensor
        if data[i][2] == 'pillow' and data[i][0] == 'data':
            # print(data[i][3])
            pillow_search_date = data[i][3].date()
            if pillow_search_date == pillow_start_date:
                if pillow_flag:
                    if "HEAD_NOT_DETECTED" in data[i][4]:
                        off_pillow += 1
                        pillow_flag = False
                        last_pillow_time = sensor_time
                else:
                    if "HEAD_NOT_DETECTED" in data[i][4]:
                        last_pillow_time = sensor_time
            else:
                pillow_record.append(off_pillow)
                pillow_start_date = pillow_search_date
                last_pillow_time = sensor_time
                off_pillow = 1
        if (sensor_time - last_pillow_time).total_seconds() > 10:
            pillow_flag = True

    mat_record.append(off_bed)
    pillow_record.append(off_pillow)
    print(mat_record)
    print(pillow_record)
    return off_bed, off_pillow


def update_num_wake_up(connection, cursor):
    select_query = "select * from ca_sleep_trend where date = %s"
    curdate = datetime.date(2019, 4, 28)
    cursor.execute(select_query, (curdate,))
    record = cursor.fetchone()
    if record is None:
        insert_query = "insert into ca_sleep_trend (patient_id, date, num_wake_up) VALUES (%s, %s, %s)"
        record_to_insert = (1, curdate, 0)
        cursor.execute(insert_query, record_to_insert)
    else:
        update_query = "update ca_sleep_trend set num_wake_up = num_wake_up + 1 where patient_id = 1 and date = %s"
        cursor.execute(update_query, (curdate,))
    connection.commit()
    print('Successfully update sleep_trend num_wake_up')


def update_num_get_out_of_bed(connection, cursor):
    select_query = "select * from ca_sleep_trend where date = %s"
    curdate = datetime.date(2019, 4, 28)
    cursor.execute(select_query, (curdate,))
    record = cursor.fetchone()
    if record is None:
        insert_query = "insert into ca_sleep_trend (patient_id, date, num_get_out_of_bed) VALUES (%s, %s, %s)"
        record_to_insert = (1, curdate, 0)
        cursor.execute(insert_query, record_to_insert)
    else:
        update_query = "update ca_sleep_trend set num_get_out_of_bed = num_get_out_of_bed + 1 where patient_id = 1 and date = %s"
        cursor.execute(update_query, (curdate,))
    connection.commit()
    print('Successfully update sleep_trend num_get_out_of_bed')


if __name__ == "__main__":
    main()
    sys.exit(0)
