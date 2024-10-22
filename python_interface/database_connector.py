import psycopg2


class DatabaseWrapper:
    def __init__(self, user, password, host, port, database, schema):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.schema = schema

        self.database = database
        self.connection = None
        self.cursor = None

        self.columns = None
        self.tables = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except:
            print('Error connecting to database')

        try:
            self.__get_tables_and_reverse_column_names__()
        except:
            print('Error fetching tables and columns')

    def __get_tables_and_reverse_column_names__(self):
        self.tables = self.fetch_table_names()
        self.columns = [None] * len(self.tables)
        for i in range(len(self.tables)):
            self.columns[i] = self.fetch_column_names(self.tables[i])
            temp = self.columns[i][::-1]
            self.columns[i] = temp

    def close(self):
        self.cursor.close()
        self.connection.close()

    def send_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('Error sending query: ', query)
            print(e)
            return None

    def fetch_column_names(self, table):
        if table not in self.tables:
            print('Table not found: ', table)
            return None
        try:
            query = f'SELECT * FROM {self.schema}.{table}'
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            self.connection.commit()
            return columns
        except Exception as e:
            print('Error fetching column names')
            print('Table not found: ', table)
            print(f'SELECT * FROM {self.schema}.{table}')
            print(e)
    
    def fetch_all(self, table):
        query = f"SELECT * FROM {self.schema}.{table}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('Error fetching all')
            print("query: ", query)
            print(e)
    
    def search_column(self, table, column, value):
        query = f"SELECT * FROM {self.schema}.{table} WHERE {column} = '{value}'"
        print(query)
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('Error searching column')
            print("query: ", query)
            print(e)
            return None
        
    def insert_row(self, table, primary_key, data):
        index = self.get_table_index(table)
        primary_key_column = self.get_primary_key(table)[0][0]

        # # Check if data exists
        search_result = self.search_column(table, primary_key_column, primary_key)
        if search_result:
            split_data = data.split(',')
            #look for differences in data
            for i in range(len(split_data)):
                #if data is different and NOT the primary key
                if split_data[i] != search_result[0][i + 1] and self.columns[index][i + 1] != primary_key_column:
                    #update the data
                    self.update_row(table, self.columns[index][i + 1], split_data[i])
        else:
            self.__insert_row__(table, [primary_key] + data.split(','))
    
    def delete_from_name(self, table, name):
        query = f"DELETE FROM {self.schema}.{table} WHERE name = '{name}'"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return name
        except Exception as e:
            print('Error deleting from name')
            print("query: ", query)
            print(e)
            return None
        return name
    
    def clear_table(self, table):
        query = f"DELETE FROM {self.schema}.{table}"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return table
        except Exception as e:
            print('Error clearing table')
            print("query: ", query)
            print(e)
            return None
    
    def fetch_table_names(self):
        query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.schema}'"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            temp = self.cursor.fetchall()
            table_list = []
            for table in temp:
                table_list.append(table[0])
            return table_list
        except Exception as e:
            return None
        
    def is_column(self, column_name):
        if column_name in self.columns:
            return True
        return False
    
    def get_table_index(self, table_name):
        for i in range(len(self.tables)):
            if self.tables[i] == table_name:
                return i
        return None
    
    def update_row(self, table, column, new_value):
        query = f"UPDATE {self.schema}.{table} SET {column} = '{new_value}'"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return new_value
        except Exception as e:
            print('Error updating row')
            print("query: ", query)
            print(e)
            return None
    
    def get_column_index(self, table_index, column_name):
        for i in range(len(self.columns[table_index])):
            if self.columns[table_index][i] == column_name:
                return i
        return None
    
    def fetch_column_name(self, table_index, column_index):
        try:
            return self.columns[table_index][column_index]
        except Exception as e:
            print('Error fetching column name')
            print(e)
            return None

    def delete_row(self, table, column, value):
        query = f"DELETE FROM {self.schema}.{table} WHERE {column} = '{value}'"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return value
        except Exception as e:
            print('Error deleting row')
            print("query: ", query)
            print(e)
            return None
        
    def get_primary_key(self, table):
        query = f"""SELECT column_name
                    FROM information_schema.table_constraints
                        JOIN information_schema.key_column_usage
                            USING (constraint_catalog, constraint_schema, constraint_name,
                                    table_catalog, table_schema, table_name)
                    WHERE constraint_type = 'PRIMARY KEY'
                    AND (table_schema, table_name) = ('{self.schema}', '{table}')
                    ORDER BY ordinal_position;"""

        try:
            return self.send_query(query)
        except Exception as e:
            print('Error getting primary key')
            print(e)
            return None
        
    def __insert_row__(self, table, values):
        data_list = [str(x) for x in values]
        data = "'" + "', '".join(data_list) + "'"
        self.insert_data(table, data)

    def update_from_id(self, table, id, column, value):
        query = f"UPDATE {self.schema}.{table} SET {column} = '{value}'"
        self.send_insert_query(query)
        return value

        
