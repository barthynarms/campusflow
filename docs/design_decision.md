# Design Decisions

Agreed by Bartholomew Akor and Godwin Ngbede before implementation.


## Ownership

| Area | Owner |
|---|---|
| Ticket creation, validation, priority engine (`tickets.py`, `test_tickets.py`) | Engineer A |
| Assignment, lifecycle, queue, reports (`workflow.py`, `reports.py`, their tests) | Engineer B |
| JSON persistence (`storage.py`, `test_storage.py`) | Engineer A |
| `main.py` menu | Shared: each fellow adds their own handler functions |
| Reviews | Each fellow reviews the other's PR |

## Data structure

- A ticket is a plain `dict` with the eight required fields.
- The ticket collection is a `list` of those dicts.
- The list is **passed into** each function as the first argument. There is no global state, so tests can build their own list.
- *Trade-off:* a list is simple and keeps creation order, but lookup is O(n). That is acceptable for a small helpdesk.

## Error handling

- Invalid input raises `ValidationError` (a subclass of `ValueError`, defined in `tickets.py`).
- Unreadable storage raises `StorageError` (defined in `storage.py`).
- `workflow.py` raises plain `ValueError`. Because `ValidationError` is a subclass of `ValueError`, the CLI catches `ValueError` for assign and status changes and `ValidationError` for creation.
- The CLI prints `Error: <message>` and continues. If `StorageError` happens at startup, it prints the message and exits without overwriting the file.
- Functions validate **before** changing any data, so a rejected action cannot corrupt stored tickets.

## Function contracts

| Function | Returns | Raises |
|---|---|---|
| `create_ticket(tickets, title, category, urgency, affected_users)` | the new ticket dict (also appended to `tickets`) | `ValidationError` |
| `calculate_priority(urgency, affected_users)` | `"critical"`, `"high"`, `"medium"` or `"low"` | `ValidationError` |
| `find_ticket(tickets, ticket_id)` | the ticket dict or `None` (ID match is case-insensitive) | none |
| `load_tickets(path)` | list of tickets; `[]` if the file is missing | `StorageError` |
| `save_tickets(path, tickets)` | `None` | `OSError` on write failure |
| `assign_ticket(tickets, ticket_id, staff_name)` | the updated ticket dict | `ValueError` (unknown ID, blank name, resolved ticket) |
| `change_status(tickets, ticket_id, new_status)` | the updated ticket dict | `ValueError` (invalid status or transition, unassigned ticket to `in_progress`) |
| `get_work_queue(tickets)` | new sorted list of unresolved tickets (priority, then numeric ID) | none |
| `build_report(tickets)` | dict with `total`, `by_status`, `by_priority` | none |
| `format_report(report)` | text for the CLI | none |

## Key decisions and reasons

- **Normalisation:** category and urgency are trimmed and case-folded, then stored in canonical form (`Network`, `high`). `affected_users` accepts the text `"4"` from the CLI but rejects `0`, negatives, decimals, text and booleans.
- **Booleans rejected:** in Python `True` is an `int`, so `True` would otherwise pass as 1 affected user.
- **ID generation:** next ID is the highest existing numeric ID + 1, not the list length. This keeps IDs unique after reload, and a rejected ticket never uses up an ID.
- **Priority is plain code:** the four rules are checked in order and the first match wins. No AI model is used at runtime.
- **Testing without `input()`:** all business logic lives in `campusflow/`. `main.py` only prompts and prints.
- **Work queue scope:** the queue includes every non-resolved ticket (`open` and `in_progress`), sorted by priority and then numeric ID so `T10` comes after `T2`.
- **Saving:** `main.py` saves after every successful create, assign and status change.
- **Persistence:** `storage.py` owns all file access. Missing file means a fresh start. Malformed or wrongly structured JSON raises `StorageError` and the file is left untouched. Saves write to a temporary file and then replace the real one, so a crash cannot leave a half-written file.
- **Runtime data is not committed:** `data/tickets.json` is in `.gitignore`.

## Branch and review workflow

- Branches are named `<type>/<issue-number>-<description>` and cut from the latest `main`.
- No direct commits to `main`. Every PR is reviewed and approved by the partner before merging.
- If `main` changes first, the author merges `main` into their branch, reruns the tests and pushes.