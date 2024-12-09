import sys
import os
# Create the trouble ticket 
def create_ticket(db_connector, source, date_detected, problem_type, description, status, resolution=None):
    init_query = """
    LOCK TABLE tracker.ticket IN EXCLUSIVE MODE;
    SELECT MAX(id) FROM tracker.ticket;
    SELECT SETVAL('tracker.ticket_id_seq', COALESCE((SELECT MAX(id) FROM tracker.ticket), 0) + 1, false);
    """
    db_connector.cursor.execute(init_query)
    db_connector.connection.commit()
    
    query = """
    INSERT INTO tracker.ticket (source, report_date, date_detected, type, description, status, resolution)
    VALUES (%s, CURRENT_DATE, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    db_connector.cursor.execute(query, (source, date_detected, problem_type, description, status, resolution))
    new_id = db_connector.cursor.fetchone()[0]  # Fetch the generated ID from the database
    db_connector.connection.commit()

    print(f"Ticket with ID {new_id} for {source} added successfully!")
    return new_id

# View all open tickets
def view_open_tickets(db_connector):
    query = "SELECT * FROM tracker.ticket WHERE status = 'open';"
    db_connector.cursor.execute(query)
    rows = db_connector.cursor.fetchall()
    
    if rows:
        data = []
        for row in rows:
            id, source, type, description, status, report_date, date_detected, date_resolved, resolution  = row
            data.append({
                'id': id,
                'source': source,
                'type': type,
                'description': description,
                'status': status,
                'report_date': format_date(report_date),
                'date_detected': date_detected,
                'date_resolved': date_resolved,
                'resolution': resolution
            })
        print(data)
        return data
    else:
        print("There are currently no open trouble tickets")
        return None

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

#formatting date
def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d') if date_obj else None