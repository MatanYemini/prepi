import aiohttp
from typing import Optional, Dict, Any, List
from urllib.parse import quote
from datetime import datetime

from config.settings import RAPIDAPI_KEY, RAPIDAPI_HOST

class LinkedInScraperService:
    def __init__(self):
        self.headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }
        self.base_url = f"https://{RAPIDAPI_HOST}"

    async def get_profile_data(self, linkedin_url: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch LinkedIn profile data using RapidAPI
        
        Args:
            linkedin_url: Full LinkedIn profile URL
            
        Returns:
            Dictionary containing profile data or None if failed
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
                        # Extract the positions data from the response
                        if 'data' in data:
                            return data['data']
                        return data
                    else:
                        error_text = await response.text()
                        print(f"Error fetching LinkedIn data: {response.status} - {error_text}")
                        return None

        except Exception as e:
            print(f"Exception in LinkedIn scraping: {str(e)}")
            return None

    @staticmethod
    def extract_key_information(profile_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Extract and structure key information from the profile data according to schema
        
        Args:
            profile_data: Raw profile data from RapidAPI
            
        Returns:
            Structured profile information
        """
        try:
            # Process positions data
            positions = []
            for pos in profile_data.get('positions', []):
                position = {
                    "companyId": pos.get('companyId'),
                    "companyName": pos.get('companyName'),
                    "companyUsername": pos.get('companyUsername'),
                    "companyURL": pos.get('companyURL'),
                    "companyLogo": pos.get('companyLogo'),
                    "companyIndustry": pos.get('companyIndustry'),
                    "companyStaffCountRange": pos.get('companyStaffCountRange'),
                    "title": pos.get('title'),
                    "multiLocaleTitle": {"en_US": pos.get('title')},
                    "multiLocaleCompanyName": {"en_US": pos.get('companyName')},
                    "location": pos.get('location'),
                    "description": pos.get('description'),
                    "employmentType": pos.get('employmentType'),
                    "start": pos.get('start', {}),
                    "end": pos.get('end', {})
                }
                positions.append(position)

            # Process education data
            educations = []
            for edu in profile_data.get('education', []):
                education = {
                    "start": edu.get('start', {}),
                    "end": edu.get('end', {}),
                    "fieldOfStudy": edu.get('fieldOfStudy'),
                    "degree": edu.get('degree'),
                    "grade": edu.get('grade'),
                    "schoolName": edu.get('schoolName'),
                    "description": edu.get('description'),
                    "activities": edu.get('activities'),
                    "url": edu.get('url'),
                    "schoolId": edu.get('schoolId')
                }
                educations.append(education)

            # Process skills data
            skills = []
            for skill in profile_data.get('skills', []):
                skill_data = {
                    "name": skill.get('name'),
                    "passedSkillAssessment": skill.get('passedSkillAssessment', False),
                    "endorsementsCount": skill.get('endorsementsCount', 0)
                }
                skills.append(skill_data)

            return {
                "id": profile_data.get('id'),
                "urn": profile_data.get('urn'),
                "username": profile_data.get('username'),
                "firstName": profile_data.get('firstName'),
                "lastName": profile_data.get('lastName'),
                "isTopVoice": profile_data.get('isTopVoice', False),
                "isCreator": profile_data.get('isCreator', False),
                "profilePicture": profile_data.get('profilePicture'),
                "backgroundImage": profile_data.get('backgroundImage', []),
                "summary": profile_data.get('summary'),
                "headline": profile_data.get('headline'),
                "geo": {
                    "country": profile_data.get('country'),
                    "city": profile_data.get('city'),
                    "full": profile_data.get('location'),
                    "countryCode": profile_data.get('countryCode')
                },
                "educations": educations,
                "position": positions,
                "fullPositions": positions,  # Using same positions data for both fields
                "skills": skills,
                "projects": profile_data.get('projects', {}),
                "supportedLocales": [
                    {
                        "country": "US",
                        "language": "en"
                    }
                ],
                "multiLocaleFirstName": {
                    "en": profile_data.get('firstName')
                },
                "multiLocaleLastName": {
                    "en": profile_data.get('lastName')
                },
                "multiLocaleHeadline": {
                    "en": profile_data.get('headline')
                }
            }
        except Exception as e:
            print(f"Error processing LinkedIn profile data: {str(e)}")
            return profile_data

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

    @staticmethod
    def extract_company_information(company_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Extract and structure key company information according to the schema
        
        Args:
            company_data: Raw company data from RapidAPI
            
        Returns:
            Structured company information
        """
        try:
            # Convert funding data if available
            funding_data = company_data.get('fundingData', {})
            if funding_data:
                last_round = funding_data.get('lastFundingRound', {})
                formatted_funding = {
                    "updatedAt": funding_data.get('updatedAt'),
                    "updatedDate": funding_data.get('updatedDate'),
                    "numFundingRounds": funding_data.get('numFundingRounds'),
                    "lastFundingRound": {
                        "investorsCrunchbaseUrl": last_round.get('investorsCrunchbaseUrl'),
                        "leadInvestors": last_round.get('leadInvestors', []),
                        "fundingRoundCrunchbaseUrl": last_round.get('fundingRoundCrunchbaseUrl'),
                        "fundingType": last_round.get('fundingType'),
                        "moneyRaised": last_round.get('moneyRaised', {}),
                        "numOtherInvestors": last_round.get('numOtherInvestors'),
                        "announcedOn": last_round.get('announcedOn', {})
                    }
                }
            else:
                formatted_funding = None

            # Format headquarters data
            hq = company_data.get('headquarter', {})
            formatted_hq = {
                "geographicArea": hq.get('geographicArea'),
                "country": hq.get('country'),
                "city": hq.get('city'),
                "postalCode": hq.get('postalCode'),
                "line1": hq.get('line1')
            }

            return {
                "success": True,
                "message": "Company data retrieved successfully",
                "data": {
                    "id": company_data.get('id'),
                    "name": company_data.get('name'),
                    "universalName": company_data.get('universalName'),
                    "linkedinUrl": company_data.get('linkedinUrl'),
                    "tagline": company_data.get('tagline'),
                    "description": company_data.get('description'),
                    "type": company_data.get('type'),
                    "phone": company_data.get('phone'),
                    "Images": {
                        "logo": company_data.get('logo'),
                        "cover": company_data.get('cover')
                    },
                    "isClaimable": company_data.get('isClaimable', False),
                    "backgroundCoverImages": company_data.get('backgroundCoverImages', []),
                    "logos": company_data.get('logos', []),
                    "staffCount": company_data.get('staffCount'),
                    "headquarter": formatted_hq,
                    "locations": company_data.get('locations', []),
                    "industries": company_data.get('industries', []),
                    "specialities": company_data.get('specialities', []),
                    "website": company_data.get('website'),
                    "founded": company_data.get('founded'),
                    "callToAction": company_data.get('callToAction', {
                        "callToActionType": None,
                        "visible": False,
                        "callToActionMessage": {
                            "textDirection": "LTR",
                            "text": ""
                        },
                        "url": ""
                    }),
                    "followerCount": company_data.get('followerCount'),
                    "staffCountRange": company_data.get('staffCountRange'),
                    "crunchbaseUrl": company_data.get('crunchbaseUrl'),
                    "fundingData": formatted_funding
                }
            }
        except Exception as e:
            print(f"Error processing company data: {str(e)}")
            return {
                "success": False,
                "message": f"Error processing company data: {str(e)}",
                "data": company_data
            }

    def clean_data(self, data: Any) -> Any:
        """Remove URLs and picture-related fields from the data"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                # Skip URL and picture-related fields
                if any(skip_key in str(key).lower() for skip_key in [
                    'url', 'picture', 'image', 'avatar', 'photo', 'profilepicture', 
                    'backgroundimage', 'logo', 'icon'
                ]):
                    continue
                # Also skip if the value is a URL string
                if isinstance(value, str) and (
                    value.startswith('http://') or 
                    value.startswith('https://') or 
                    'linkedin.com' in value.lower()
                ):
                    continue
                # Recursively clean nested dictionaries and lists
                if isinstance(value, (dict, list)):
                    cleaned[key] = self.clean_data(value)
                else:
                    cleaned[key] = value
            return cleaned
        elif isinstance(data, list):
            return [self.clean_data(item) for item in data]
        return data

    async def enrich_profile_with_company_data(
        self, 
        profile_data: Dict[Any, Any], 
        focus_area: Optional[str] = None, 
        cleanup: bool = False
    ) -> Dict[Any, Any]:
        """
        Enrich profile data with company information
        """
        # Clean the input data first if cleanup is requested        
        if cleanup:
            profile_data = self.clean_data(profile_data)

        # Get positions from either positions or experience field
        positions = profile_data.get('positions', []) or profile_data.get('experience', [])
        if not positions:
            profile_data['positions'] = []  # Ensure positions exists even if empty
            return profile_data

        enriched_positions = []
        for position in positions:
            company_username = position.get('companyUsername')
            enriched_position = {
                "title": position.get('title'),
                "description": position.get('description'),
                "start": position.get('start'),
                "end": position.get('end'),
                "location": position.get('location'),
                "employmentType": position.get('employmentType'),
                "companyName": position.get('companyName')
            }

            if company_username:
                company_data = await self.get_company_data(company_username)
                if company_data and 'data' in company_data:
                    company_info = company_data['data']
                    if cleanup:
                        company_info = self.clean_data(company_info)
                    
                    extra_info = {
                        "headquarter": company_info.get('headquarter', {}),
                        "locations": company_info.get('locations', []),
                        "industries": company_info.get('industries', []),
                        "specialities": company_info.get('specialities', []),
                        "founded": company_info.get('founded'),
                        "followerCount": company_info.get('followerCount'),
                        "staffCountRange": company_info.get('staffCountRange'),
                        "fundingData": company_info.get('fundingData', {})
                    }
                    
                    enriched_position["extraInfo"] = extra_info

            enriched_positions.append(enriched_position)

        profile_data['positions'] = enriched_positions
        
        # Clean the final output if cleanup is requested
        if cleanup:
            profile_data = self.clean_data(profile_data)
        
        return profile_data

    def filter_by_focus_area(self, enriched_position: Dict[str, Any], focus_area: str) -> Dict[str, Any]:
        """
        Filter or prioritize data based on the focus area
        
        Args:
            enriched_position: The enriched position data
            focus_area: The focus area to prioritize
            
        Returns:
            Filtered or prioritized position data
        """
        if focus_area == "conversation":
            # Prioritize roles that involve customer interaction or communication
            if any(keyword in enriched_position['personal']['title'].lower() for keyword in ["sales", "customer", "client", "relationship", "communication"]):
                return enriched_position
            else:
                # Deprioritize roles that are less relevant to conversation
                return {}
        # Add more focus areas as needed
        return enriched_position 