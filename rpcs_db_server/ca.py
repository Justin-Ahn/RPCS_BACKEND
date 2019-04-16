import psycopg2

try:
    connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from hs_events"

    cursor.execute(postgreSQL_select_Query)
    print('Selecting rows from hs table using cursor.fetchall')
    hs_events = cursor.fetchall()
    for row in hs_events:
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

