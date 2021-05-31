import sqlite3
from sqlite3 import Error


# import sqlite3

# def create():
#     try:
#         c.execute("""CREATE TABLE mytable
#                  (start, end, score)""")
#     except:
#         pass

# def insert():
#     c.execute("""INSERT INTO mytable (start, end, score)
#               values(1, 99, 123)""")

# def select(verbose=True):
#     sql = "SELECT * FROM mytable"
#     recs = c.execute(sql)
#     if verbose:
#         for row in recs:
#             print (row)

# db_path = r'/Users/dantonucci/Alubel/Alubel_credentials.db'
# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# create()
# insert()
# conn.commit() #commit needed
# select()
# c.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r'/Users/dantonucci/Alubel/Alubel_credentials.db'

    sql_create_credentials_table = """ CREATE TABLE IF NOT EXISTS Credentials (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL                                        
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_credentials_table)
    else:
        print("Error! cannot create the database connection.")
        
        
        
# INSERT CREDENTIALS 

# """ 
# INSEWRT INTO Credentials ()

# """

# def insert():
#     c.execute("""INSERT INTO mytable (start, end, score)
#               values(1, 99, 123)""")

if __name__ == '__main__':
    main()