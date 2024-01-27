import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    print('Configuration initialization...')
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    # conn_params = config()
    # print(conn_params)
    # Check if the database exists
    if not database_exists(db):  # create_or_check
        print(f"Database '{db['database']}' does not exist. Creating...")
        create_database(db)
    else:
        print(f"Database '{db['database']}' already exists.")
        pass
    return db


def db_connect(db_params):
    return psycopg2.connect(**db_params)


def database_exists(db_params):
    try:
        connection = db_connect(db_params)
        # connection = psycopg2.connect(
        #     user=db_params['user'],
        #     password=db_params['password'],
        #     host=db_params['host'],
        #     port=db_params['port'],
        #     database=db_params['database']
        # )
        connection.close()
        return True
    except psycopg2.OperationalError:
        return False


def create_table():
    conn_params = config()
    connection = db_connect(conn_params)
    cursor = connection.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            name VARCHAR,
            surname VARCHAR,
            email_address VARCHAR NOT NULL UNIQUE
        );
        '''
    cursor.execute(create_table_query)
    # print('The table clients has been inserted.')

    create_table_query2 = '''
        CREATE TABLE IF NOT EXISTS clients_inquiry_support (
            id SERIAL PRIMARY KEY,
            email_address VARCHAR NOT NULL UNIQUE, 
            name VARCHAR, 
            subject VARCHAR NOT NULL, 
            intention VARCHAR NOT NULL, 
            is_solved BOOLEAN NOT NULL
        )
    '''
    cursor.execute(create_table_query2)
    # print('The table client_inquiry has been inserted.')
    cursor.connection.commit()

    cursor.close()
    connection.close()


def create_database(db_params):
    # PostgreSQL connection
    # connection = db_connect(db_config)
    connection = psycopg2.connect(
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        # Checking if the database already exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (db_params['database'],))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_params['database'])))
        #     print(f"Database '{db_config['database']}' created successfully.")
        # else:
        #     print(f"Database '{db_config['database']}' already exists.")
    except psycopg2.Error as e:
        pass
        print(f"Error creating or checking database: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        create_table()


def insert_data(table_name, data, condition=None):
    conn_params = config()
    connection = db_connect(conn_params)
    cursor = connection.cursor()
    try:
        # Check if the row with the specified condition already exists
        select_query = sql.SQL("SELECT * FROM {} WHERE {}").format(
            sql.Identifier(table_name),
            sql.SQL(' AND ').join(
                sql.SQL("{} = {}").format(sql.Identifier(column), sql.Placeholder())
                for column in condition.keys()
            )
        )

        cursor.execute(select_query, list(condition.values()))
        existing_row = cursor.fetchone()

        if existing_row:
            print("Row already exists. Skipping insertion.")
        else:
            # Insert the data if the row does not exist
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                sql.SQL(', ').join(sql.Placeholder() * len(data))
            )

            cursor.execute(insert_query, list(data.values()))
            connection.commit()
            print("Data inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()


def update_data(table_name, data, condition):       # condition ex: 'id': 1
    db_params = config()
    connection = db_connect(db_params)
    cursor = connection.cursor()
    try:
        set_clause = sql.SQL(', ').join(
            sql.SQL("{} = {}").format(sql.Identifier(column), sql.Placeholder())
            for column in data.keys()
        )

        update_query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            sql.Identifier(table_name),
            set_clause,
            sql.SQL(' AND ').join(
                sql.SQL("{} = {}").format(sql.Identifier(column), sql.Placeholder())
                for column in condition.keys()
            )
        )

        cursor.execute(update_query, list(data.values()) + list(condition.values()))
        connection.commit()
        # print("Data updated successfully.")
    except psycopg2.Error as e:
        pass
        # print(f"Error updating data: {e}")
    finally:
        cursor.close()
        connection.close()


def get_data(table_name):
    db_params = config()
    connection = db_connect(db_params)
    cursor = connection.cursor()
    sql_query = sql.SQL("SELECT * FROM {};").format(
            sql.Identifier(table_name)
            )
    cursor.execute(sql_query)
    data = cursor.fetchall()
    # print(data)
    return data

