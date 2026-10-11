PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
ALLOWED_TRANSITIONS = {
    "open": ["in_progress"],
    "in_progress": ["resolved"],
    "resolved": ["open"],  # explicit reopen
}


def find_ticket(tickets, ticket_id):
    """Return the ticket with this ID, or raise ValueError if unknown."""
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if ticket["id"] == wanted:
            return ticket
    raise ValueError(f"Ticket '{ticket_id}' was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a staff member (F3)."""
    ticket = find_ticket(tickets, ticket_id)
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must not be blank.")
    if ticket["status"] == "resolved":
        raise ValueError("A resolved ticket must be reopened before it can be changed.")
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Move a ticket through open -> in_progress -> resolved, or reopen it (F4)."""
    ticket = find_ticket(tickets, ticket_id)
    new_status = str(new_status).strip().lower()

    if new_status not in ALLOWED_TRANSITIONS:
        raise ValueError(
            f"Invalid status '{new_status}'. Use open, in_progress or resolved."
        )

    current = ticket["status"]
    if new_status not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"Cannot move a ticket from {current} to {new_status}.")

    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign the ticket to someone before starting work on it.")

    ticket["status"] = new_status
    return ticket


def _id_number(ticket):
    """'T012' -> 12, so T10 sorts after T2 (numeric, not text, order)."""
    return int(ticket["id"][1:])


def get_work_queue(tickets):
    """Unresolved tickets: critical -> high -> medium -> low, then lower ID first (F5).

    Assumption: "open, unresolved" means every ticket that is not resolved
    (open and in_progress). Change the filter to == "open" if your team
    decides the queue should show only open tickets.
    """
    pending = [t for t in tickets if t["status"] != "resolved"]
    return sorted(pending, key=lambda t: (PRIORITY_ORDER[t["priority"]], _id_number(t)))