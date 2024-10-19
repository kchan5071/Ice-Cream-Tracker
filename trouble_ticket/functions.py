# Create the trouble ticket 
def create_ticket(db_connector, id, source, date_detected, problem_type, description, status, resolution=None):
    query = """
    INSERT INTO tracker.ticket (id, source, report_date, date_detected, type, description, status, resolution)
    VALUES (%s, %s, CURRENT_DATE, %s, %s, %s, %s, %s);
    """
    db_connector.cursor.execute(query, (id, source, date_detected, problem_type, description, status, resolution))
    db_connector.connection.commit()

    print(f"Ticket with ID {id} for {source} added successfully!")

# View all open tickets
def view_open_tickets(db_connector):
    query = "SELECT * FROM tracker.ticket WHERE status = 'open';"
    db_connector.cursor.execute(query)
    rows = db_connector.cursor.fetchall()
    for row in rows:
        print(row)

# Delete a ticket 
def delete_ticket(db_connector, ticket_id):
    query = "DELETE FROM tracker.ticket WHERE id = %s;"
    db_connector.cursor.execute(query, (ticket_id,))
    db_connector.connection.commit()
    print(f"Ticket with ID {ticket_id} has been deleted.")


# Update the status of a ticket
def update_ticket_status(db_connector, ticket_id, new_status, resolution=None):
    query = """
    UPDATE tracker.ticket 
    SET status = %s, resolution = %s, date_resolved = CASE WHEN %s = 'closed' THEN CURRENT_DATE ELSE NULL END
    WHERE id = %s;
    """
    db_connector.cursor.execute(query, (new_status, resolution, new_status, ticket_id))
    db_connector.connection.commit()
    print(f"Ticket {ticket_id} updated to {new_status}")


# Search for a ticket by customer name or problem 
def search_tickets(db_connector, source=None, problem_type=None):
    query = "SELECT * FROM tracker.ticket WHERE "
    conditions = []
    if source:
        conditions.append(f"source = '{source}'")
    if problem_type:
        conditions.append(f"type = '{problem_type}'")
    
    if conditions:
        query += " AND ".join(conditions)
    else:
        query += "1=1"  # Fallback condition

    db_connector.cursor.execute(query)
    rows = db_connector.cursor.fetchall()
    for row in rows:
        print(row)
 
def summary_of_open_tickets(db_connector):
    query = """
    SELECT type, COUNT(*) AS total_open
    FROM tracker.ticket
    WHERE status = 'open'
    GROUP BY type;
    """
    db_connector.cursor.execute(query)
    rows = db_connector.cursor.fetchall()
    
    # Access tuple elements using integer indices
    for row in rows:
        print(f"{row[0]}: {row[1]} open tickets")

# Summary Report
def generate_statistical_report(db_connector):
    query = """
    SELECT 
        type, 
        COUNT(*) AS total_problems, 
        ROUND(AVG(EXTRACT(DAY FROM age(date_resolved, report_date)))) AS avg_time_to_close,
        ROUND(AVG(EXTRACT(DAY FROM age(CURRENT_DATE, report_date)))) AS avg_open_days
    FROM tracker.ticket
    WHERE status = 'closed'
    GROUP BY type;
    """
    db_connector.cursor.execute(query)
    rows = db_connector.cursor.fetchall()

    # Access tuple elements using integer indices
    for row in rows:
        print(f"Type: {row[0]}, Total: {row[1]}, Avg Time to Close: {row[2]} days, Avg Open Days: {row[3]} days")
