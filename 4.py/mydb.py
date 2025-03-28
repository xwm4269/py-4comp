import sqlite3 as sq

data_base = sq.connect("pisos.db")
cursor = data_base.cursor()

cursor.executescript("""
BEGIN;
CREATE TABLE
IF NOT EXISTS
User(id INTEGER PRIMARY KEY, login TEXT , password TEXT);
                     
CREATE TABLE
IF NOT EXISTS
Admin(id INTEGER PRIMARY KEY, login TEXT , password TEXT);
                     
CREATE TABLE
IF NOT EXISTS
Equipment(id INTEGER PRIMARY KEY, name TEXT);
                     
CREATE TABLE
IF NOT EXISTS
Type(id INTEGER PRIMARY KEY, name TEXT);
                     
CREATE TABLE
IF NOT EXISTS
Status(id INTEGER PRIMARY KEY, name TEXT);
                     
CREATE TABLE
IF NOT EXISTS
Request(id INTEGER PRIMARY KEY,
        datatime TEXT, 
        equipment_id INTEGER, 
        type_id INTEGER,
        description TEXT,
        user_name TEXT,
        status TEXT,
        admin TEXT,
        comment TEXT
        );
COMMIT;
""")
data_base.commit()

def get_from_db(
        fields, 
        table, 
        where = ""
    ):
    """
    fields - ["","",]
    table - User
    where = login = "{var}"
    
    """
    fields = ",".join(fields)
    log_in_values = cursor.execute(f"""
    SELECT {fields}
    FROM {table}
    WHERE {where}    
    """)
    return log_in_values.fetchall()

def insert_value(login, password):
    cursor.execute(f"""
    INSERT INTO User(login, password) 
    VALUES("{login}", "{password}")
    """)
    data_base.commit()

def check_and_get_user(login):
    user = cursor.execute(f'SELECT id from User WHERE login="{login}"').fetchone()
    if user:
        return user[0]
    else:
        return None

def search_user_for_login(login, password):
    user = cursor.execute(f'SELECT id from User WHERE login="{login}" AND password="{password}"').fetchone()
    if user:
        return user[0]
    else:
        return None

def search_admin_for_login(login, password):
    user = cursor.execute(f'SELECT id from Admin WHERE login="{login}" AND password="{password}"').fetchone()
    if user:
        return user[0]
    else:
        return None
    
def equipment_and_type_serch():
    equipment = cursor.execute(f'SELECT name from Equipment').fetchall()
    type = cursor.execute(f'SELECT name from Type').fetchall()

    return equipment, type

def insert_request(data_time, equipment_id, type_id, dadescriptionta_time, user_name):
    cursor.execute(f""" INSERT INTO Request(datatime, equipment_id, type_id, description, user_name)
        VALUES('{data_time}', '{equipment_id}','{type_id}','{dadescriptionta_time}','{user_name}')
    """)
    data_base.commit()

def my_request(user):
    x = cursor.execute(f""" SELECT * from Request WHERE user_name="{user}"
    """).fetchall()
    return x
    

    

