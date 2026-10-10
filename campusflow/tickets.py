
import re

CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}
URGENCY_LEVELS = ("low", "medium", "high")


class ValidationError(ValueError):
    """Raised when ticket input is invalid."""


# ---------- validation / normalisation ----------

def validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValidationError("Title must not be blank.")
    return title.strip()


def normalize_category(category):
    key = category.strip().lower() if isinstance(category, str) else None
    if key not in CATEGORIES:
        raise ValidationError(
            "Invalid category. Choose one of: " + ", ".join(CATEGORIES.values()) + "."
        )
    return CATEGORIES[key]


def normalize_urgency(urgency):
    value = urgency.strip().lower() if isinstance(urgency, str) else None
    if value not in URGENCY_LEVELS:
        raise ValidationError(
            "Invalid urgency. Choose one of: " + ", ".join(URGENCY_LEVELS) + "."
        )
    return value


def validate_affected_users(affected_users):
    """Return a positive int. Rejects 0, negatives, decimals, bools and text."""
    msg = "affected_users must be a positive whole number (1 or more)."
    if isinstance(affected_users, bool):
        raise ValidationError(msg)
    if isinstance(affected_users, int):
        value = affected_users
    elif isinstance(affected_users, str):
        text = affected_users.strip()
        if not (text.isascii() and text.isdigit()):  # rejects "3.5", "-2", "abc"
            raise ValidationError(msg)
        value = int(text)
    else:  # floats (even 3.0), None, lists...
        raise ValidationError(msg)
    if value <= 0:
        raise ValidationError(msg)
    return value


# ---------- priority engine ----------

def calculate_priority(urgency, affected_users):
    """Apply the rules in order; the first match wins."""
    urgency = normalize_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    if urgency == "high" and affected_users >= 10:      # Rule 1
        return "critical"
    if urgency == "high" or affected_users >= 10:       # Rule 2
        return "high"
    if urgency == "medium" or affected_users >= 3:      # Rule 3
        return "medium"
    return "low"                                        # Rule 4


# ---------- ID generation ----------

def next_ticket_id(tickets):
    """Return the next unique ID (T001, T002, ...) based on the highest existing one.

    Using max()+1 (not len()+1) keeps IDs unique after a reload.
    """
    highest = 0
    for ticket in tickets:
        match = re.fullmatch(r"T(\d+)", str(ticket.get("id", "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"T{highest + 1:03d}"


# ---------- creation ----------

def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate input, build the ticket, append it to `tickets` and return it.

    Raises ValidationError (and leaves `tickets` untouched) on invalid input.
    """
    title = validate_title(title)
    category = normalize_category(category)
    urgency = normalize_urgency(urgency)
    affected_users = validate_affected_users(affected_users)
    priority = calculate_priority(urgency, affected_users)

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def find_ticket(tickets, ticket_id):
    """Return the ticket with this ID (case-insensitive) or None."""
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if ticket["id"] == wanted:
            return ticket
    return None