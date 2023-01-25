import sqlite3

def db_conn(db_name, hw_data, pkg_data):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    insert_into_hw_db(hw_data, cur)
    insert_into_pkg_db(pkg_data, cur)
    conn.commit()
    conn.close()


def insert_into_hw_db(hw_data, c):
    try:
        c.execute("""CREATE TABLE hwinfo (
                    element text
                    )""")
    except:
        print("Table 'hwinfo' already exists")


    c.execute("SELECT * FROM hwinfo")
    result = c.fetchall()

    if len(result) == 0:
        for item in hw_data:
            if item == "HWINFO":
                continue
            c.execute(f"INSERT INTO hwinfo VALUES ('{item}')")
            print(f"[DB-LOG] Successfully inserted '{item}' into table 'hwinfo'")
    else:
        c.execute("SELECT * FROM hwinfo")
        for item in hw_data:
            if item == "HWINFO":
                continue
            result = c.fetchone()
            if type(result) is type(None):
                continue
            if item != result[0]:
                c.execute(f"INSERT INTO hwinfo VALUES ('{item}')")
                print(f"[DB-LOG] Successfully inserted '{item}' into table 'hwinfo'")


def insert_into_pkg_db(pkg_data, c):
    try:
        c.execute("""CREATE TABLE packages (
                    name text,
                    version text
                    )""")
    except:
        print("Table 'packages' already exists")

    c.execute("SELECT * FROM packages")
    result = c.fetchall()

    if len(result) == 0:
        for key in pkg_data.keys():
            if key == "HEADER":
                continue
            c.execute(f"INSERT INTO packages VALUES ('{key}', '{pkg_data[key]}')")
            print(f"[DB-LOG] Successfully inserted '{key}: {pkg_data[key]}' into table 'packages'")
    else:
        c.execute("SELECT * FROM packages")
        for key in pkg_data.keys():
            if key == "HEADER":
                continue
            result = c.fetchone()
            if type(result) is type(None):
                continue
            if key != result[0]:
                c.execute(f"INSERT INTO packages VALUES ('{key}', '{pkg_data[key]}')")
                print(f"[DB-LOG] Successfully inserted '{key}: {pkg_data[key]}' into table 'packages'")
