# helper functions for the sign up and login process
# checks to see if a user with said username exists
def check_for_username(db_connector, employee_table,name, user_name):
        # db_connector is chosen database wrapper
        query = f"""SELECT * FROM {db_connector.schema}.{employee_table}
                    WHERE {name} = '{user_name}'
                    """
        db_connector.cursor.execute(query)
        success = db_connector.cursor.fetchall()
        return success # will return an array of users if a user is found

# checks to see if a user with said username and password exists
def check_for_user(db_connector, employee_table, name, user_name, password, user_password):
        # db_connector is chosen database wrapper
        query = f"""SELECT * FROM {db_connector.schema}.{employee_table}
                    WHERE {name} = '{user_name}' AND {password} = '{user_password}'
                    """
        db_connector.cursor.execute(query)
        success = db_connector.cursor.fetchall()
        return success # will return an array of users if a user is found

# checks to see if a user is an admin
def check_for_user_admin(db_connector, employee_table, name, user_name, password,  user_password):
        # db_connector is chosen database wrapper
        query = f"""SELECT * FROM {db_connector.schema}.{employee_table}
                    WHERE {name} = '{user_name}' AND {password} = '{user_password}' AND admin = 'true'
                    """
        db_connector.cursor.execute(query)
        success = db_connector.cursor.fetchall()
        return success # will return an array of users if a user is found

# adds a new Ice Track user (nonadmin)
def add_employee(db_connector, employee_table, user_name, password):
    try:
        query = f"""
                INSERT INTO {db_connector.schema}.{employee_table} 
                (name, password)
                VALUES (%s, %s);
                """
        db_connector.cursor.execute(query, (user_name, password))
        db_connector.connection.commit() 
        
        # verifies the insert
        success = check_for_user(db_connector, employee_table, 'name', user_name, 'password', password)
        if success:
            print(user_name + " was added")
            return "New employee added!"
        else:
            print("Could not add employee")
            return "New employee not added."
    except Exception as e:
        db_connector.connection.rollback()  # rollback in the case of failure
        print(f"Error occurred: {e}")
        return f"Error occurred: {e}"



