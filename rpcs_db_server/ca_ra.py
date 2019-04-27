import psycopg2
import sys
import  time
import datetime
import pytz

def main():
    try:
        connection = psycopg2.connect(user = 'rpcs', password = 'rpcs2019', host = 'localhost', port =  '', database ='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgreSQL',error)
    else:
       #ar_analysis(connection, cursor)
        print('success')
        stove(connection, cursor)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')

def stove(connection, cursor):
    select_query = "select * from hs_events"
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
#    timestr_low = "time2019-04-21 18:00"
#    time_low = time.strptime(timestr_low,"time%Y-%m-%d %H:%M")
#    time_lower = datetime.datetime(*time_low[:6])
#    time_lower = time_lower.replace(tzinfo = pytz.timezone('UTC'))
    
#    timestr_high = "time2019-04-22 06:00"
#    time_high = time.strptime(timestr_high,"time%Y-%m-%d %H:%M")
#    time_higher = datetime.datetime(*time_high[:6])
#    time_higher = time_higher.replace(tzinfo = pytz.timezone('UTC'))

#    timestr_sec = "time2019-04-22 18:00"
#    time_sec = time.strptime(timestr_sec,"time%Y-%m-%d %H:%M")
#    time_secer = datetime.datetime(*time_sec[:6])
#    time_secer = time_secer.replace(tzinfo = pytz.timezone('UTC'))

#analyze night
#    for i in range(len(time_prime)):
#        if time_prime[i] < time_higher and time_prime[i] > time_lower and average_value[i] > 30:
#            print("danger in night")
#            print(time_prime[i])
#            break
   
#analyze day
#    for i in range(len(time_prime)):
#        if time_prime[i] > time_higher and time_prime[i] < time_secer and average_value[i] > 30:
#            for j in range(len(time_motion)):
#                if time_motion[j] < time_prime[i] and time_motion[j+1]>time_prime[i]:
#                    if type_motion[j] == 'U' and type_motion[j+1] == 'M':
#                        print('danger in day')
#                        break
                    
#analyze night
    for i in range(len(time_prime)):
        if check_night(time_prime[i]) is True:
            if average_value[i] > 30:
                print("danger in night")
                print(time_prime[i])
                break
#analyze day
    for in in range(len(time_prime)):
        if check_night(time_prime[i]) is False:
            if average_value[i] > 30:
                for j in range(len(time_motion)):
                    if time_motion[j] < time_prime[i] and time_motion[j+1]>time_prime[i]:
                        if type_motion[j] == 'U' and type_motion[j+1] == 'M':
                            print('danger in day')
                            break
                    






#    if time_prime[0]> time_lower:
#        print("gfd")
#    if time_prime[0] < time_prime[1]:
#        print('aa')
#    else:
#        print("bb")

                


    
   





   # print(index_left)
   # print(index_right)

if __name__ == "__main__":
    main()
    sys.exit(0)

   
    

                    
                    

