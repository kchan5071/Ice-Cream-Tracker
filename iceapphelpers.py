# helpers
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()  # Adjust format as needed
    except ValueError:
        print("Invalid date format:", date_str)
        return None


def check_for_user(db_connector, table, column, primary_key, column2, value):
        # self is chosen database wrapper
        # table is the employee table in this case that were looking for
        # primary key is the username were checking for
        # column is the column name that we're searching in for username
        # value is the password were checking for
        # column2 is the column name that we're searching in for password
        query = f"""SELECT * FROM {db_connector.schema}.{table}
                    WHERE {column} = '{primary_key}' AND {column2} = '{value}'"""
        db_connector.cursor.execute(query)
        success = db_connector.cursor.fetchall()
        print(success)
        return success # will return true if a user is found
