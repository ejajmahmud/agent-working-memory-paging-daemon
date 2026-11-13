"""Unit tests for agent-working-memory-paging-daemon."""
import unittest
from agent_working_memory_paging_daemon.daemon import MemoryPagingDaemon

class TestMemoryPagingDaemon(unittest.TestCase):
    def setUp(self):
        self.daemon = MemoryPagingDaemon(max_pages_in_ram=2)

    def test_put_and_get_ram(self):
        self.daemon.put("p1", "data1")
        self.assertEqual(self.daemon.get("p1"), "data1")
        self.assertEqual(self.daemon.page_fault_count, 0)

    def test_eviction_and_page_fault(self):
        self.daemon.put("p1", "d1")
        self.daemon.put("p2", "d2")
        self.daemon.put("p3", "d3")  # p1 should be evicted to swap
        self.assertNotIn("p1", self.daemon.ram)
        self.assertIn("p1", self.daemon.swap_store)
        res = self.daemon.get("p1")
        self.assertEqual(res, "d1")
        self.assertEqual(self.daemon.page_fault_count, 1)
        self.assertIn("p1", self.daemon.ram)

    def test_unknown_page(self):
        self.assertIsNone(self.daemon.get("missing"))

if __name__ == "__main__":
    unittest.main()
