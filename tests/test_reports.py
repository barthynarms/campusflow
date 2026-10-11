import unittest

from campusflow.reports import build_report, format_report


def make_ticket(ticket_id, priority, status):
    return {
        "id": ticket_id,
        "title": "Sample problem",
        "category": "Network",
        "urgency": "low",
        "affected_users": 1,
        "priority": priority,
        "status": status,
        "assigned_to": None,
    }


class TestReports(unittest.TestCase):
    def test_empty_report_has_zero_counts(self):
        report = build_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(sum(report["by_status"].values()), 0)
        self.assertEqual(sum(report["by_priority"].values()), 0)

    def test_report_counts_by_status_and_priority(self):
        tickets = [
            make_ticket("T001", "critical", "open"),
            make_ticket("T002", "critical", "in_progress"),
            make_ticket("T003", "low", "resolved"),
        ]
        report = build_report(tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["critical"], 2)
        self.assertEqual(report["by_priority"]["high"], 0)
        self.assertEqual(report["by_priority"]["low"], 1)

    def test_format_report_shows_total(self):
        text = format_report(build_report([make_ticket("T001", "high", "open")]))
        self.assertIn("Total tickets: 1", text)


if __name__ == "__main__":
    unittest.main()