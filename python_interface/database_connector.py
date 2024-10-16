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
            print(f'SELECT * FROM {table}')
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
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('Error searching column')
            print("query: ", query)
            print(e)
            return None
        
    def insert_data(self, table, data):
        index = self.get_table_index(table)
        query = f"INSERT INTO {self.schema}.{table} ({','.join(self.columns[index])}) VALUES ({data})"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return data
        except Exception as e:
            print('Error inserting data')
            print("query: ", query)
            print(e)
            return None
    
    def delete_from_name(self, table, name):
        query = f"DELETE FROM {self.schema}.{table} WHERE name = '{name}'"
        self.send_insert_query(query)
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

        
