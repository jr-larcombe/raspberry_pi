import sqlite3

#def read_sql(sql_file):
#    sqlFile = open('sql/' + sql_file, 'r')
#    sqlText = sqlFile.read()
#    sqlText = sqlText.replace('\n','')
#    #sqlText = sqlText.split(';')
#    sqlFile.close()
#    return sqlText

setup_sql = """
CREATE TABLE IF NOT EXISTS f_temps (
    read_time float PRIMARY KEY,
    temp_1 float,
    temp_2 float
    );
"""

insert_sql = """
INSERT INTO f_temps VALUES (%s,%s,%s)
"""

read_sql = """
SELECT * FROM f_temps
"""

def execute_sql(sql_string, read=False):
    sql_string = sql_string.replace('\n','')
    conn=sqlite3.connect("temp_sensor.db")
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
    
def insert_readings(read_time, temp_1, temp_2):
    sql_string = insert_sql % (read_time, temp_1, temp_2)
    execute_sql(sql_string)
    
def view_readings():
    return execute_sql(read_sql, read=True)

# Setup inital connection    
execute_sql(setup_sql)