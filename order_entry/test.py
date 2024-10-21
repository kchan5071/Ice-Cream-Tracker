import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path so python_interface is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.database_connector import DatabaseWrapper


def main():

    # if testing on computer ensure correct user (should match linux username)
    user = 'admin'
    password = 'password'
    host = 'localhost'
    port = '5432'
    database = 'icecreamtracker'
    schema = 'tracker'


    db_connector = DatabaseWrapper(user, password, host, port, database, schema)
    db_connector.connect()
    db_connector.insert_data(table, data)

    #print table names
    print("Tables: ")
    print(db_connector.tables)

    #print column names
    print("Columns: ")
    for i in range(len(db_connector.tables)):
        print(db_connector.columns[i])

    db_connector.insert_row('customer', ['wendy', 'dave', 'ok'])


    print(db_connector.search_column('customer', 'company', 'wendy'))

    db_connector.delete_row('customer', 'password', 'dave')

    # print("Data: ")
    # print(db_connector.fetch_all(table))

    # #add second row
    # name = 'Mikaela Software'
    # order_number = 125
    # time = '2021-06-01 11:00:00'

    # data = f"'{name}', '{time}', {order_number}"
    # db_connector.insert_data(table, data)

    # print("Data: ")
    # print(db_connector.fetch_all(table))

    # #delete row
    # db_connector.delete_row(table, 'name', 'Sigfriend Software')
    
    # print("Data: ")
    # print(db_connector.fetch_all(table))

    # #clear table
    # db_connector.clear_table(table)

    db_connector.close()

if __name__ == '__main__':
    main()