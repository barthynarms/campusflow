import os
import tempfile
import unittest

from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import create_ticket


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = os.path.join(self.dir.name, "data", "tickets.json")

    def test_missing_file_gives_empty_list(self):
        self.assertEqual(load_tickets(self.path), [])

    def test_save_and_reload_preserves_tickets(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)
        create_ticket(tickets, "Slow PC", "Hardware", "low", 1)
        tickets[0]["assigned_to"] = "Ada"
        save_tickets(self.path, tickets)
        self.assertEqual(load_tickets(self.path), tickets)

    def test_create_after_reload_does_not_duplicate_ids(self):
        tickets = []
        create_ticket(tickets, "One", "Other", "low", 1)
        create_ticket(tickets, "Two", "Other", "low", 1)
        save_tickets(self.path, tickets)
        reloaded = load_tickets(self.path)
        new = create_ticket(reloaded, "Three", "Other", "low", 1)
        self.assertEqual(new["id"], "T003")
        ids = [t["id"] for t in reloaded]
        self.assertEqual(len(ids), len(set(ids)))

    def test_malformed_json_raises_and_file_is_untouched(self):
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            f.write("{not valid json")
        with self.assertRaises(StorageError):
            load_tickets(self.path)
        with open(self.path) as f:
            self.assertEqual(f.read(), "{not valid json")

    def test_wrong_structure_raises(self):
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            f.write('{"id": "T001"}')
        with self.assertRaises(StorageError):
            load_tickets(self.path)

    def test_empty_ticket_list_round_trips(self):
        save_tickets(self.path, [])
        self.assertEqual(load_tickets(self.path), [])

    def test_save_leaves_no_temp_files(self):
        save_tickets(self.path, [{"id": "T001"}])
        self.assertEqual(os.listdir(os.path.dirname(self.path)), ["tickets.json"])


if __name__ == "__main__":
    unittest.main()