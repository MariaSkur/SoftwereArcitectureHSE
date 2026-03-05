import unittest
import requests
import time

BASE_URL = "http://localhost:5000/api/events"

class TestEventAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ждём, пока backend и БД полностью поднимутся
        time.sleep(5)

    def test_1_create_event(self):
        payload = {
            "name": "Test Event",
            "date": "2025-12-31",
            "location": "Test Location",
            "description": "Test Description"
        }
        resp = requests.post(BASE_URL, json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], payload["name"])
        # сохраним id для следующих тестов
        self.__class__.event_id = data["id"]

    def test_2_get_events(self):
        resp = requests.get(BASE_URL)
        self.assertEqual(resp.status_code, 200)
        events = resp.json()
        self.assertIsInstance(events, list)
        self.assertGreaterEqual(len(events), 1)

    def test_3_get_event_by_id(self):
        if not hasattr(self, 'event_id'):
            self.skipTest("No event id from previous test")
        resp = requests.get(f"{BASE_URL}/{self.event_id}")
        self.assertEqual(resp.status_code, 200)
        event = resp.json()
        self.assertEqual(event["id"], self.event_id)

    def test_4_update_event(self):
        if not hasattr(self, 'event_id'):
            self.skipTest("No event id from previous test")
        payload = {
            "name": "Updated Event",
            "date": "2026-01-01",
            "location": "Updated Location",
            "description": "Updated Description"
        }
        resp = requests.put(f"{BASE_URL}/{self.event_id}", json=payload)
        self.assertEqual(resp.status_code, 200)
        updated = resp.json()
        self.assertEqual(updated["name"], payload["name"])

    def test_5_delete_event(self):
        if not hasattr(self, 'event_id'):
            self.skipTest("No event id from previous test")
        resp = requests.delete(f"{BASE_URL}/{self.event_id}")
        self.assertEqual(resp.status_code, 204)
        # проверяем, что удалено
        resp = requests.get(f"{BASE_URL}/{self.event_id}")
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
