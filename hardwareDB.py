import pymysql
import pandas as pd
import time


def view_table(cursor):
    if(cursor is None):
        print("Connect to DB first, use the 'connect()' method")
        return
    print(get_dataframe(cursor))


def connect():
    db = pymysql.connect(host="testing-database.cg1cr4po4sbk.us-east-2.rds.amazonaws.com",
                         user="admin", password="admin1234")
    cursor = db.cursor()
    cursor.execute("use hardware_db")
    print("Connected to hardware_db database")
    return cursor, db


def get_dataframe(cursor):
    cursor.execute("use hardware_db")
    cursor.execute("select * from sensor_data")
    df = pd.DataFrame(cursor.fetchall(), columns=[
                      'id', 'temp', 'dist1', 'dist2', 'dist3', 'p_sensor', 'time'])
    return df


def insert(temp_v, dist1_v, dist2_v, dist3_v, p_sensor_v):
    db = pymysql.connect(host="testing-database.cg1cr4po4sbk.us-east-2.rds.amazonaws.com",
                         user="admin", password="admin1234")
    cursor = db.cursor()
    cursor.execute("use hardware_db")
    sql = "insert into sensor_data(temp,dist1,dist2,dist3,p_sensor) values ({},{},{},{},{})".format(
        temp_v, dist1_v, dist2_v, dist3_v, p_sensor_v)
    cursor.execute(sql)
    db.commit()
    print("OK. Data inserted!")
    cursor.close()
    db.close()


def clear_table(db):
    if(db is None):
        print("Connect to DB first, use the 'connect()' method")
        return
    db[0].execute("TRUNCATE TABLE sensor_data")
    db[1].commit()
    print("OK. Table is cleared!")


def live_table(cursor, seconds):
    while (True):
        print(get_dataframe(cursor))
        time.sleep(seconds)


def get_last(id):
    # Connect to database
    db = pymysql.connect(host="testing-database.cg1cr4po4sbk.us-east-2.rds.amazonaws.com",
                         user="admin", password="admin1234")
    cursor = db.cursor()
    cursor.execute("use hardware_db")

    # Get the last element in the table if id counter beats adding things to dB
    cursor.execute("SELECT id FROM sensor_data ORDER BY id DESC LIMIT 1")
    last_id = cursor.fetchall()
    last_id = last_id[0][0]

    if (id > last_id):
        id = last_id

    sql = "SELECT temp, dist1, dist2, dist3 FROM sensor_data where id = {}".format(
        id)

    cursor.execute(sql)
    ans = cursor.fetchall()
    cursor.close()
    db.close()
    return ans


# db = connect()
# cursor = db[0]

data = get_last(2)
print(data)

# df = get_dataframe(cursor)


# for x in range(1, 6):
#     element = get_last("time", x, cursor)
#     print(element)
#     time.sleep(1)
