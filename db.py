import sqlite3 as sq

data_base = sq.connect("user.db")
cur = data_base.cursor()

cur.executescript("""
BEGIN;
CREATE TABLE
IF NOT EXISTS
User(id INTEGER PRIMARY KEY, login TEXT , password TEXT);
CREATE TABLE
IF NOT EXISTS
Admin(id INTEGER PRIMARY KEY, login TEXT , password TEXT);
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
    log_in_values = cur.execute(f"""
    SELECT {fields}
    FROM {table}
    WHERE {where}    
    """)
    return log_in_values.fetchall()



def insert_value(login, password):
    cur.execute(f"""
    INSERT INTO User(login, password) 
    VALUES("{login}", "{password}")
    """)
    data_base.commit()
    

def check_and_get_user(login):
    user = cur.execute(f'SELECT id from User WHERE login="{login}"').fetchone()
    if user:
        return user[0]
    else:
        return None



def search_user_for_login(login, password):
    user = cur.execute(f'SELECT id from User WHERE login="{login}" AND password="{password}"').fetchone()
    if user:
        return user[0]
    else:
        return None

def search_admin_for_login(login, password):
    user = cur.execute(f'SELECT id from Admin WHERE login="{login}" AND password="{password}"').fetchone()
    if user:
        return user[0]
    else:
        return None



def check_log_in():
    log_in_values = cur.execute(f"""
    SELECT login, password
    FROM User
    """).fetchall()
    chmo = cur.execute(f"""
    SELECT login, password
    FROM Admin
    """).fetchall()
    print(log_in_values, chmo)