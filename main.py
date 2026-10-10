
from campusflow.tickets import ValidationError, create_ticket, find_ticket

DATA_FILE = "data/tickets.json"


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
    print(f"Created {ticket['id']} with priority {ticket['priority']}.")
    # save_tickets(DATA_FILE, tickets)   # enable once storage.py is merged


def handle_list_tickets(tickets):
    if not tickets:
        print("No tickets yet.")
        return
    for t in tickets:
        print(f"{t['id']} | {t['priority']:<8} | {t['status']:<11} | {t['title']}")


def handle_view_ticket(tickets):
    ticket = find_ticket(tickets, input("Ticket ID: "))
    if ticket is None:
        print("Error: unknown ticket ID.")
        return
    for key, value in ticket.items():
        print(f"{key}: {value}")



MENU = """
=== CampusFlow ===
1. Create ticket
2. List tickets
3. View ticket
0. Exit
"""

ACTIONS = {
    "1": handle_create_ticket,
    "2": handle_list_tickets,
    "3": handle_view_ticket,
}


def main():
    tickets = []  # replace with: tickets = load_tickets(DATA_FILE)
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