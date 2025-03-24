import unittest
from fastapi.testclient import TestClient
from src.services.agents.text_cleaning_agent import TextCleaningAgent
from src.main import app
import os

class TestLinkedInScrapers(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
    def test_get_profile_data(self):
        response = self.client.post(
            "/linkedin/profile",
            json={"profile_url": "https://www.linkedin.com/in/matan-yemini"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Write response to JSON file in test folder
        test_folder = "test"
        file_path = os.path.join(test_folder, "profile_data_response.json")
        
        # Ensure test directory exists
        os.makedirs(test_folder, exist_ok=True)
        
        with open(file_path, "w") as file:
            file.write(str(data))
            
    
    def test_cleaned_get_profile_data(self):
        response = self.client.post(
            "/linkedin/profile",
            json={"profile_url": "https://www.linkedin.com/in/matan-yemini", "cleanup": True, "include_posts": False}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Write response to JSON file in test folder
        test_folder = "test"
        file_path = os.path.join(test_folder, "profile_data_response.json")
        
        # Ensure test directory exists
        os.makedirs(test_folder, exist_ok=True)
        
        with open(file_path, "w") as file:
            file.write(str(data))
    
    
    
    
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
        
        # Write the response to a text file in this folder
        with open("uncleaned_data.txt", "w") as file:
            file.write(str(data))
        
        # clean the data using the text cleaning agent
        text_cleaning_agent = TextCleaningAgent()
        cleaned_data = text_cleaning_agent.clean_text(data, "uncleaned_data.txt")
        
        #save the cleaned data to a file
        with open("cleaned_data.txt", "w") as file:
            file.write(str(cleaned_data))

if __name__ == "__main__":
    unittest.main() 