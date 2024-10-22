from database_connector import DatabaseWrapper


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
    # db_connector.insert_data(table, data)

    #print table names
    print("Tables: ")
    print(db_connector.tables)

    #print column names
    print("Columns: ")
    for i in range(len(db_connector.tables)):
        print(db_connector.tables[i], db_connector.columns[i])

    #print all data in table
    print("Data: ")
    for table in db_connector.tables:
        print("Table: ", table)
        data = db_connector.fetch_all(table)
        print(data)

    #test insertion
    table = 'customer'
    data = 'burger, ok'
    db_connector.insert_data(table, 'bk',data)
    
    #print data from table
    print("Data: ")
    data = db_connector.fetch_all(table)
    print(data)

    db_connector.close()

    



    

if __name__ == '__main__':
    main()