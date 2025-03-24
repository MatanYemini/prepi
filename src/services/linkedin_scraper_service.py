import aiohttp
from typing import Optional, Dict, Any
from urllib.parse import quote

from config.settings import RAPIDAPI_KEY, RAPIDAPI_HOST
from models.linkedin_types import CleanedLinkedInProfileScraperResponse, LinkedInProfileScraperResponse

USE_TYPES = False

class LinkedInScraperService:
    def __init__(self):
        self.headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }
        self.base_url = f"https://{RAPIDAPI_HOST}"

    async def get_profile_data(self, linkedin_url: str, cleanup: bool = False):
        """
        Fetch LinkedIn profile data using RapidAPI
        
        Args:
            linkedin_url: Full LinkedIn profile URL
            
        Returns:
            LinkedInProfileResponse object containing profile data or None if failed
        """
        try:
            # Ensure the URL is a string
            if not isinstance(linkedin_url, str):
                linkedin_url = str(linkedin_url)
            
            # Encode the LinkedIn URL
            encoded_url = quote(linkedin_url)
            
            # Construct the API endpoint
            endpoint = f"/get-profile-data-by-url?url={encoded_url}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if USE_TYPES:
                            typed_data = None
                            # Extract the positions data from the response and validate with Pydantic
                            if 'data' in data:
                                typed_data = LinkedInProfileScraperResponse(**data['data'])
                            typed_data = LinkedInProfileScraperResponse(**data)
                            data = typed_data.model_dump()
                            
                        if cleanup:
                            data = self.clean_data(data)
                        return data
                    else:
                        error_text = await response.text()
                        print(f"Error fetching LinkedIn data: {response.status} - {error_text}")
                        return None

        except Exception as e:
            print(f"Exception in LinkedIn scraping: {str(e)}")
            return None


    async def get_company_data(self, company_username: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch LinkedIn company data using RapidAPI
        
        Args:
            company_username: Company username/handle from LinkedIn
            
        Returns:
            Dictionary containing company data or None if failed
        """
        try:
            endpoint = f"/get-company-details?username={quote(company_username)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        print(f"Error fetching company data: {response.status} - {error_text}")
                        return None

        except Exception as e:
            print(f"Exception in company data fetching: {str(e)}")
            return None

    
    def clean_data(self, data: LinkedInProfileScraperResponse):
        """Remove URLs and sensitive fields from the data"""            
        # Convert to dict, remove unwanted fields
        data_dict = data
        
        # Remove top-level fields
        data_dict.pop('profilePicture', None)
        data_dict.pop('profilePictures', None)
        data_dict.pop('backgroundImage', None)
        data_dict.pop('projects', None)  # Remove projects entirely
        
        # Clean skills
        if 'skills' in data_dict:
            for skill in data_dict['skills']:
                skill.pop('passedSkillAssessment', None)
                skill.pop('endorsementsCount', None)
        
        # Clean educations
        if 'educations' in data_dict:
            for education in data_dict['educations']:
                education.pop('url', None)
                education.pop('schoolId', None)
                education.pop('logos', None)
        
        # Clean positions
        if 'positions' in data_dict:
            for position in data_dict['positions']:
                position.pop('logos', None)
                position.pop('companyLogo', None)
                if 'extraInfo' in position and position['extraInfo']:
                    position['extraInfo'].pop('website', None)
                    
        
        if 'fullPositions' in data_dict:
            for position in data_dict['fullPositions']:
                if 'extraInfo' in position and position['extraInfo']:
                    position['extraInfo'].pop('website', None)
        
        
        return data_dict


    async def get_profile_posts(self, username: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch all posts for a given LinkedIn profile username using RapidAPI
        
        Args:
            username: LinkedIn profile username
            
        Returns:
            Dictionary containing posts data or None if failed
        """
        try:
            endpoint = f"/get-profile-posts?username={quote(username)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        print(f"Error fetching profile posts: {response.status} - {error_text}")
                        return None

        except Exception as e:
            print(f"Exception in fetching profile posts: {str(e)}")
            return None

    async def get_company_posts(self, company_username: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch all posts for a given LinkedIn company username using RapidAPI
        
        Args:
            company_username: LinkedIn company username
            
        Returns:
            Dictionary containing company posts data or None if failed
        """
        try:
            endpoint = f"/get-company-posts?username={quote(company_username)}&start=0"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        print(f"Error fetching company posts: {response.status} - {error_text}")
                        return None

        except Exception as e:
            print(f"Exception in fetching company posts: {str(e)}")
            return None

    async def add_posts_to_profile_data(self, profile_data):
        """
        Add posts to the profile data by fetching them using the profile's username
        
        Args:
            profile_data: The profile data dictionary
            
        Returns:
            Profile data with posts added
        """
        try:
            username = profile_data.get('username')
            if not username:
                print("No username found in profile data.")
                return profile_data

            posts = await self.get_profile_posts(username)
            if posts:
                print("added profile posts to profile data")
                        # Clean posts if they exist
                for post in posts:
                    # Remove specific URLs from post
                    post.pop('profilePicture', None)
                    post.pop('url', None)
                    post.pop('postUrl', None)
                    post.pop('shareUrl', None)
                    
                    # If there are any nested author or shared post objects
                    if 'author' in post:
                        post['author'].pop('profilePicture', None)
                        post['author'].pop('url', None)
                    if 'sharedPost' in post and post['sharedPost']:
                        post['sharedPost'].pop('profilePicture', None)
                        post['sharedPost'].pop('url', None)
                        post['sharedPost'].pop('postUrl', None)
                        post['sharedPost'].pop('shareUrl', None)
                        
                profile_data['posts'] = posts
                
            else:
                print("No posts found for the given username.")

            return profile_data

        except Exception as e:
            print(f"Exception in adding posts to profile data: {str(e)}")
            return profile_data 

    async def add_company_posts_to_profile_data(self, profile_data):
        """
        Add posts of the most recent company the user has been at to the profile data
        
        Args:
            profile_data: The profile data dictionary
            
        Returns:
            Profile data with company posts added
        """
        try:
            # Get the most recent position
            positions = profile_data.get('position', [])
            if not positions:
                print("No positions found in profile data.")
                return profile_data

            # Assuming the most recent position is the first in the list
            recent_position = positions[0]
            company_username = recent_position.get('companyUsername')
            if not company_username:
                print("No company username found in the most recent position.")
                return profile_data

            company_posts = await self.get_company_posts(company_username)
            if company_posts:
                print("added company posts to profile data")
                profile_data['recentCompanyPosts'] = company_posts
            else:
                print("No posts found for the recent company.")

            return profile_data

        except Exception as e:
            print(f"Exception in adding company posts to profile data: {str(e)}")
            return profile_data 