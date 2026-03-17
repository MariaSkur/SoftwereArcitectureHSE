import unittest
import requests
import time

BASE_URL = "http://localhost:5000/api/projects"

class TestProjectAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(5)

    def test_1_create_project(self):
        payload = {
            "name": "Молодёжный форум",
            "date": "2025-06-15",
            "location": "ДК «Мир»",
            "description": "Обсуждение инициатив"
        }
        resp = requests.post(BASE_URL, json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], payload["name"])
        self.__class__.project_id = data["id"]

    def test_2_get_projects(self):
        resp = requests.get(BASE_URL)
        self.assertEqual(resp.status_code, 200)
        projects = resp.json()
        self.assertIsInstance(projects, list)
        self.assertGreaterEqual(len(projects), 1)

    def test_3_get_project_by_id(self):
        if not hasattr(self, 'project_id'):
            self.skipTest("No project id from previous test")
        resp = requests.get(f"{BASE_URL}/{self.project_id}")
        self.assertEqual(resp.status_code, 200)
        project = resp.json()
        self.assertEqual(project["id"], self.project_id)

    def test_4_update_project(self):
        if not hasattr(self, 'project_id'):
            self.skipTest("No project id from previous test")
        payload = {
            "name": "Обновлённый форум",
            "date": "2025-07-20",
            "location": "Парк культуры",
            "description": "Обновлённое описание"
        }
        resp = requests.put(f"{BASE_URL}/{self.project_id}", json=payload)
        self.assertEqual(resp.status_code, 200)
        updated = resp.json()
        self.assertEqual(updated["name"], payload["name"])

    def test_5_delete_project(self):
        if not hasattr(self, 'project_id'):
            self.skipTest("No project id from previous test")
        resp = requests.delete(f"{BASE_URL}/{self.project_id}")
        self.assertEqual(resp.status_code, 204)
        resp = requests.get(f"{BASE_URL}/{self.project_id}")
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
