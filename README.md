# campusflow

Project Goal: CampusFlow

CampusFlow is a Python command-line ticket manager that replaces Learn2Earn’s informal, easily lost technical support reports with a structured, reliable system. CampusFlow lets campus staff record problems such as Wi-Fi outages, faulty laptops, broken development environments, and inaccessible platforms. It prioritizes work, assigns responsibility, and tracks each issue through to resolution.

# Team
| Fellow | Role | Main contribution |
|---|---|---|
| `Bartholomew Akor` | Engineer A | Ticket creation, input validation, priority engine, JSON persistence, docs, `tests/test_tickets.py`, `tests/test_storage.py` |
| `Godwin Ngbede` | Engineer B | Assignment, status workflow, work queue, reports, `tests/test_workflow.py`, `tests/test_reports.py` |


## Requirements and setup

- Python 3.8 or newer. Only the standard library is used (`json`, `unittest`), so there is nothing to install.
- Clone the repo and run everything from the repository root:

```bash
git clone https://github.com/barthynarms/campusflow.git
cd campusflow
```

## Run the app

```bash
python main.py
```

The menu keeps running until you choose **0 (Exit)**.

| Option | What it does |
|---|---|
| 1 | Create a ticket (validated, priority calculated, unique ID) |
| 2 | List all tickets |
| 3 | View one ticket's details |
| 4 | Assign a ticket to a staff member |
| 5 | Change status / reopen |
| 6 | Show the work queue |
| 7 | Show reports |
| 0 | Exit |



## Run the tests

```bash
python -m unittest discover -s tests -v
```

| Test file | Covers |
|---|---|
| `tests/test_tickets.py` | Priority rules and boundaries, field validation, normalisation, unique sequential IDs, rejected input leaving data unchanged |
| `tests/test_storage.py` | Save/reload round trip, missing file, malformed JSON, wrong structure, IDs after reload |
| `tests/test_workflow.py` | Assignment and status transitions |
| `tests/test_reports.py` | Work queue ordering and reports |

## Ticket rules

**Fields:** `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.

- IDs are generated automatically: `T001`, `T002`, ...
- Categories: `Network`, `Hardware`, `Software`, `Other` (case-insensitive input).
- Urgency: `low`, `medium`, `high` (case-insensitive input).
- Title must not be blank. `affected_users` must be a positive whole number.

**Priority** (rules checked in order, first match wins):

1. high urgency **and** 10+ affected users → `critical`
2. high urgency **or** 10+ affected users → `high`
3. medium urgency **or** 3+ affected users → `medium`
4. everything else → `low`

This is ordinary Python logic in `campusflow/tickets.py`, not an AI model.

**Status workflow:** `open → in_progress → resolved`.
A ticket must be assigned before it can move to `in_progress`.
A resolved ticket can only change after an explicit reopen that sets it back to `open`.

## Where tickets are saved

Tickets are stored in `data/tickets.json`, which is ignored by Git.
It is loaded on startup and saved after changes. To start fresh, close the program and
delete `data/tickets.json`. If the file contains invalid JSON, the app shows a clear
error and does **not** overwrite it.

## Project layout

```
main.py                  CLI menu
campusflow/tickets.py    validation, priority engine, ID generation, ticket creation
campusflow/workflow.py   assignment and status transitions
campusflow/reports.py    work queue and reports
campusflow/storage.py    JSON load/save
tests/                   unittest test files
docs/                    design decisions and AI learning log
``` 

## Known limitations

- Single user, single process; there is no file locking, so two copies running at once could overwrite each other's changes.
- Tickets cannot be edited (title, category, urgency) or deleted after creation.
- Loading only checks that the file holds a list of tickets with IDs; it does not re-validate every field.
- Text-only interface with no search or filtering.

## Future improvements

- Edit and delete tickets with an audit trail.
- Re-validate all fields when loading.
- Filter and search by category, assignee or status.
- Export reports to CSV.