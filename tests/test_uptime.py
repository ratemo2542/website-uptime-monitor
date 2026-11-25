import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
import main

class UptimeTests(unittest.TestCase):
    def test_records_status_and_latency(self):
        response = Mock(status_code=200)
        with patch.object(main.requests, "get", return_value=response):
            status, latency, error = main.check("https://example.com")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(latency, 0)
        self.assertEqual(error, "")

    def test_records_network_failure(self):
        with patch.object(main.requests, "get", side_effect=main.requests.Timeout("timeout")):
            status, latency, error = main.check("https://example.com")
        self.assertEqual(status, "")
        self.assertIn("timeout", error)

if __name__ == "__main__":
    unittest.main()
