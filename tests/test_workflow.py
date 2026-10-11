import unittest

from campusflow.workflow import (
    assign_ticket,
    change_status,
    find_ticket,
    get_work_queue,
)


def make_ticket(ticket_id, priority="low", status="open", assigned_to=None):
    return {
        "id": ticket_id,
        "title": "Sample problem",
        "category": "Network",
        "urgency": "low",
        "affected_users": 1,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestAssign(unittest.TestCase):
    def test_assign_sets_staff_name(self):
        tickets = [make_ticket("T001")]
        assign_ticket(tickets, "T001", "  Amina  ")
        self.assertEqual(tickets[0]["assigned_to"], "Amina")

    def test_assign_unknown_ticket_rejected(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T999", "Amina")

    def test_assign_blank_name_rejected_and_ticket_unchanged(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "   ")
        self.assertIsNone(tickets[0]["assigned_to"])

    def test_find_ticket_accepts_lowercase_id(self):
        tickets = [make_ticket("T001")]
        self.assertIs(find_ticket(tickets, "t001"), tickets[0])


class TestWorkflow(unittest.TestCase):
    def test_unassigned_ticket_cannot_start(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "open")

    def test_assigned_ticket_full_lifecycle(self):
        tickets = [make_ticket("T001", assigned_to="Amina")]
        change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(tickets[0]["status"], "resolved")

    def test_cannot_skip_open_to_resolved(self):
        tickets = [make_ticket("T001", assigned_to="Amina")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "resolved")
        self.assertEqual(tickets[0]["status"], "open")

    def test_invalid_status_name_rejected(self):
        tickets = [make_ticket("T001", assigned_to="Amina")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "finished")

    def test_resolved_ticket_can_be_reopened(self):
        tickets = [make_ticket("T001", status="resolved", assigned_to="Amina")]
        change_status(tickets, "T001", "open")
        self.assertEqual(tickets[0]["status"], "open")

    def test_resolved_ticket_cannot_be_assigned_until_reopened(self):
        tickets = [make_ticket("T001", status="resolved", assigned_to="Amina")]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "Bola")
        self.assertEqual(tickets[0]["assigned_to"], "Amina")

    def test_resolved_ticket_cannot_jump_to_in_progress(self):
        tickets = [make_ticket("T001", status="resolved", assigned_to="Amina")]
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "in_progress")


class TestQueue(unittest.TestCase):
    def test_queue_sorted_by_priority_then_numeric_id(self):
        tickets = [
            make_ticket("T001", "low"),
            make_ticket("T010", "critical"),
            make_ticket("T002", "critical"),
            make_ticket("T003", "high"),
            make_ticket("T004", "medium"),
        ]
        ids = [t["id"] for t in get_work_queue(tickets)]
        self.assertEqual(ids, ["T002", "T010", "T003", "T004", "T001"])

    def test_queue_excludes_resolved_tickets(self):
        tickets = [
            make_ticket("T001", "critical", status="resolved"),
            make_ticket("T002", "low"),
        ]
        ids = [t["id"] for t in get_work_queue(tickets)]
        self.assertEqual(ids, ["T002"])

    def test_queue_does_not_reorder_the_original_list(self):
        tickets = [make_ticket("T001", "low"), make_ticket("T002", "critical")]
        get_work_queue(tickets)
        self.assertEqual([t["id"] for t in tickets], ["T001", "T002"])

    def test_empty_queue(self):
        self.assertEqual(get_work_queue([]), [])


if __name__ == "__main__":
    unittest.main()