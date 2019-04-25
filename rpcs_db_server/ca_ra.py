import psycopg2
import sys
def main():
    try:
        connection = psycopg2.connect(user = 'rpcs', password = 'rpcs2019', host = 'localhost', port =  '', database ='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL',error)
    else:
       #ar_analysis(connection, cursor)
        print('success')
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')
if __name__ == "__main__":
    main()
    sys.exit(0)
