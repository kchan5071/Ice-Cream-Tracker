import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.database_connector import DatabaseWrapper
from functions import create_ticket, view_open_tickets, update_ticket_status, search_tickets, summary_of_open_tickets, generate_statistical_report, delete_ticket


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

    # TEST CASES

    current_id = 10
    # Create a new trouble ticket
    create_ticket(
        db_connector,                 
        id = current_id,
        source='Customer A',           
        date_detected='2024-09-28',    
        problem_type='shipping',       
        description='Package not received',  
        status='open'                  #
    )

    # View all open tickets
    print("Open Tickets:")
    view_open_tickets(db_connector)

    # Update the status of a ticket 
    update_ticket_status(db_connector, 1, 'closed', 'Issue resolved')

    # Search for tickets by customer name 
    print("\nSearch Results for Customer A:")
    search_tickets(db_connector, source='Customer A')

    # View a summary of open tickets 
    print("\nSummary of Open Tickets:")
    summary_of_open_tickets(db_connector)

    # Generate a statistical report for closed tickets
    print("\nStatistical Report for Closed Tickets:")
    generate_statistical_report(db_connector)

    # Delete a ticket
    print("\nDeleting ticket with ID 10...")
    delete_ticket(db_connector, 10)

    # View all open tickets again to confirm deletion
    print("\nOpen Tickets After Deletion:")
    view_open_tickets(db_connector)
   
    db_connector.close()

if __name__ == '__main__':
    main()