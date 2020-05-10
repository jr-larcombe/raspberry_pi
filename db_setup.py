import sqlite3

#def read_sql(sql_file):
#    sqlFile = open('sql/' + sql_file, 'r')
#    sqlText = sqlFile.read()
#    sqlText = sqlText.replace('\n','')
#    #sqlText = sqlText.split(';')
#    sqlFile.close()
#    return sqlText

db_path = "/home/pi/Documents/temp_sensor/"

setup_sql = """
CREATE TABLE IF NOT EXISTS f_temps (
    read_time int,
    sensor text,
    unit text,
    temp_2 float,
    PRIMARY KEY (read_time, sensor)
    );
"""

insert_sql = """
INSERT INTO f_temps VALUES (%s,'%s','%s',%s)
"""

read_sql = """
SELECT * FROM f_temps
"""

# Define function to execute a create, insert or read sql statement
def execute_sql(sql_string, read=False):
    sql_string = sql_string.replace('\n','')
    conn=sqlite3.connect(db_path + "temp_sensor.db")
    cur=conn.cursor()
    try:
        cur.execute(sql_string)
    except sqlite3.IntegrityError as e:
        print('Integrity Error, no insert: ', e)
    if read:
        rows = cur.fetchall()
    else:
        conn.commit()
        rows = None
    return rows

# Define function to insert readings into database  
def insert_readings(read_time, sensor, unit, value):
    sql_string = insert_sql % (read_time, sensor, unit, value)
    execute_sql(sql_string)
    return None

# Define function to get readings from database    
def view_readings():
    return execute_sql(read_sql, read=True)

# Setup inital connection and create table if doesn't exist
execute_sql(setup_sql)
