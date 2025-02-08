import unittest
from fastapi.testclient import TestClient
from src.main import app
import os

class TestLinkedInScrapers(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_linkedin_profile(self):
        response = self.client.post("/linkedin/profile", json={"profile_url": "https://www.linkedin.com/in/someuser"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_get_linkedin_company(self):
        response = self.client.post("/linkedin/company", json={"company_username": "somecompany"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])

    def test_get_enriched_linkedin_profile(self):
        response = self.client.post(
            "/linkedin/enriched-profile", 
            json={"profile_url": "https://www.linkedin.com/in/matan-yemini", "focus_area": "conversation"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Write the response to a text file
        test_folder = "test"
        file_path = os.path.join(test_folder, "enriched_profile_response.txt")
        
        # Ensure the test directory exists
        os.makedirs(test_folder, exist_ok=True)
        
        with open(file_path, "w") as file:
            file.write(str(data))
        
        # Additional assertions can be added here
        self.assertIn("positions", data)

    def test_get_enriched_linkedin_profile_with_cleanup(self):
        response = self.client.post(
            "/linkedin/enriched-profile", 
            json={
                "profile_url": "https://www.linkedin.com/in/matan-yemini", 
                "focus_area": "conversation"
            },
            params={"cleanup": True}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify positions/experience data exists
        self.assertTrue(
            'positions' in data or 'experience' in data or 'enrichedPositions' in data,
            "No positions/experience data found in response"
        )
        
        # Verify cleanup worked
        def check_no_urls_or_dimensions(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # No URL-like fields
                    self.assertFalse(
                        any(url_key in str(key).lower() 
                            for url_key in ['url', 'picture', 'image', 'avatar', 'photo']),
                        f"Found URL-like field: {key}"
                    )
                    # Recursively check nested objects
                    if isinstance(value, (dict, list)):
                        check_no_urls_or_dimensions(value)
            elif isinstance(obj, list):
                for item in obj:
                    check_no_urls_or_dimensions(item)
        
        check_no_urls_or_dimensions(data)

if __name__ == "__main__":
    unittest.main() 