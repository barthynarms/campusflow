"""CampusFlow CLI entry point.

main.py only shows the menu, collects typed input and calls the functions in the
campusflow package. Business rules live in campusflow/, so they can be unit-tested
without input().
"""
from campusflow import workflow
from campusflow.reports import build_report, format_report
from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import ValidationError, create_ticket, find_ticket

DATA_FILE = "data/tickets.json"


def _save(tickets):
    """Write tickets to disk, reporting (not crashing on) a write failure."""
    try:
        save_tickets(DATA_FILE, tickets)
    except OSError as error:
        print(f"Warning: could not save tickets ({error}).")


# ---------- F1: create ----------

def handle_create_ticket(tickets):
    print("\n--- Create ticket ---")
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected = input("Affected users (whole number, 1 or more): ")
    try:
        ticket = create_ticket(tickets, title, category, urgency, affected)
    except ValidationError as error:
        print(f"Error: {error}")
        return
    _save(tickets)
    print(f"Created {ticket['id']} with priority {ticket['priority']}.")


# ---------- F2: list / view ----------

def handle_list_tickets(tickets):
    if not tickets:
        print("No tickets yet.")
        return
    for t in tickets:
        assignee = t["assigned_to"] or "unassigned"
        print(f"{t['id']} | {t['priority']:<8} | {t['status']:<11} | {assignee:<12} | {t['title']}")


def handle_view_ticket(tickets):
    ticket = find_ticket(tickets, input("Ticket ID: "))
    if ticket is None:
        print("Error: unknown ticket ID.")
        return
    for key, value in ticket.items():
        print(f"{key}: {value}")


# ---------- F3: assign ----------

def handle_assign_ticket(tickets):
    ticket_id = input("Ticket ID: ")
    staff_name = input("Assign to (staff name): ")
    try:
        ticket = workflow.assign_ticket(tickets, ticket_id, staff_name)
    except ValueError as error:   # ValidationError is a ValueError too
        print(f"Error: {error}")
        return
    _save(tickets)
    print(f"{ticket['id']} assigned to {ticket['assigned_to']}.")


# ---------- F4: workflow ----------

def handle_change_status(tickets):
    ticket_id = input("Ticket ID: ")
    new_status = input("New status (open/in_progress/resolved; use open to reopen): ")
    try:
        ticket = workflow.change_status(tickets, ticket_id, new_status)
    except ValueError as error:
        print(f"Error: {error}")
        return
    _save(tickets)
    print(f"{ticket['id']} is now {ticket['status']}.")


# ---------- F5: work queue ----------

def handle_work_queue(tickets):
    queue = workflow.get_work_queue(tickets)
    if not queue:
        print("The work queue is empty.")
        return
    print("\n--- Work queue (critical first) ---")
    for position, t in enumerate(queue, start=1):
        print(f"{position}. {t['id']} | {t['priority']:<8} | {t['status']:<11} | {t['title']}")


# ---------- F6: reports ----------

def handle_report(tickets):
    print()
    print(format_report(build_report(tickets)))


MENU = """
=== CampusFlow ===
1. Create ticket
2. List tickets
3. View ticket
4. Assign ticket
5. Change status
6. Work queue
7. Report
0. Exit
"""

ACTIONS = {
    "1": handle_create_ticket,
    "2": handle_list_tickets,
    "3": handle_view_ticket,
    "4": handle_assign_ticket,
    "5": handle_change_status,
    "6": handle_work_queue,
    "7": handle_report,
}


def main():
    try:
        tickets = load_tickets(DATA_FILE)   # F7: missing file -> fresh start
    except StorageError as error:
        print(f"Error: {error}")
        return   # stop without overwriting the damaged file
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option, try again.")
        else:
            action(tickets)


if __name__ == "__main__":
    main()