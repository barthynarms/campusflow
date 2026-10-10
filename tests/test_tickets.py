import unittest

from campusflow.tickets import (
    ValidationError,
    calculate_priority,
    create_ticket,
    find_ticket,
    next_ticket_id,
)


class TestPriorityEngine(unittest.TestCase):
    def test_high_urgency_12_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_boundary_10_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_urgency_2_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_10_users_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_low_urgency_4_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_medium_urgency_1_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_low_urgency_3_users_boundary_is_medium(self):
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_urgency_1_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")


class TestCreateTicket(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def test_valid_ticket_has_all_fields_and_defaults(self):
        t = create_ticket(self.tickets, "Campus Wi-Fi is down", "Network", "high", 15)
        self.assertEqual(
            t,
            {
                "id": "T001",
                "title": "Campus Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
        )
        self.assertEqual(self.tickets, [t])

    def test_ids_are_sequential_and_unique(self):
        ids = [create_ticket(self.tickets, f"Issue {i}", "Other", "low", 1)["id"] for i in range(3)]
        self.assertEqual(ids, ["T001", "T002", "T003"])

    def test_id_continues_after_existing_tickets_loaded(self):
        self.tickets.extend([{"id": "T001"}, {"id": "T007"}])
        self.assertEqual(next_ticket_id(self.tickets), "T008")

    def test_input_is_normalised(self):
        t = create_ticket(self.tickets, "  Broken laptop  ", " hArDwArE ", " HIGH ", " 4 ")
        self.assertEqual(t["title"], "Broken laptop")
        self.assertEqual(t["category"], "Hardware")
        self.assertEqual(t["urgency"], "high")
        self.assertEqual(t["affected_users"], 4)

    def test_invalid_affected_users_rejected(self):
        for bad in (0, -3, "0", "-1", "2.5", 2.5, 3.0, "abc", "", None, True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    create_ticket(self.tickets, "Printer jam", "Hardware", "low", bad)
        self.assertEqual(self.tickets, [])

    def test_blank_title_rejected(self):
        for bad in ("", "   ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    create_ticket(self.tickets, bad, "Network", "low", 1)
        self.assertEqual(self.tickets, [])

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValidationError):
            create_ticket(self.tickets, "Help", "Plumbing", "low", 1)
        self.assertEqual(self.tickets, [])

    def test_invalid_urgency_rejected(self):
        with self.assertRaises(ValidationError):
            create_ticket(self.tickets, "Help", "Other", "urgent", 1)
        self.assertEqual(self.tickets, [])

    def test_rejected_ticket_does_not_consume_or_corrupt_ids(self):
        create_ticket(self.tickets, "First", "Other", "low", 1)
        with self.assertRaises(ValidationError):
            create_ticket(self.tickets, "Bad", "Other", "low", 0)
        second = create_ticket(self.tickets, "Second", "Other", "low", 1)
        self.assertEqual(second["id"], "T002")
        self.assertEqual(len(self.tickets), 2)

    def test_find_ticket(self):
        t = create_ticket(self.tickets, "Find me", "Software", "medium", 2)
        self.assertIs(find_ticket(self.tickets, "t001"), t)
        self.assertIsNone(find_ticket(self.tickets, "T999"))


if __name__ == "__main__":
    unittest.main()