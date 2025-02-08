from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

from services.linkedin_scraper_service import LinkedInScraperService
from models.linkedin_types import LinkedInProfileResponse, LinkedInCompanyResponse

router = APIRouter(prefix="/linkedin", tags=["linkedin"])

class LinkedInProfileRequest(BaseModel):
    profile_url: HttpUrl
    focus_area: Optional[str] = None
    cleanup: bool = Optional[Query(False, description="Whether to clean up URLs and images from the response")]

class LinkedInCompanyRequest(BaseModel):
    company_username: str

@router.post("/profile", response_model=LinkedInProfileResponse)
async def get_linkedin_profile(request: LinkedInProfileRequest):
    """
    Fetch LinkedIn profile data for a given profile URL
    """
    scraper = LinkedInScraperService()
    profile_data = await scraper.get_profile_data(str(request.profile_url))
    
    if not profile_data:
        raise HTTPException(
            status_code=404,
            detail="Could not fetch LinkedIn profile data"
        )
    
    return scraper.extract_key_information(profile_data)

@router.post("/company", response_model=LinkedInCompanyResponse)
async def get_linkedin_company(request: LinkedInCompanyRequest):
    """
    Fetch LinkedIn company data for a given company username
    """
    scraper = LinkedInScraperService()
    company_data = await scraper.get_company_data(request.company_username)
    
    if not company_data:
        return {
            "success": False,
            "message": "Could not fetch LinkedIn company data",
            "data": {}
        }
    
    return scraper.extract_company_information(company_data)

@router.get("/company/{company_username}", response_model=LinkedInCompanyResponse)
async def get_linkedin_company_by_username(company_username: str):
    """
    Fetch LinkedIn company data for a given company username using GET
    """
    scraper = LinkedInScraperService()
    company_data = await scraper.get_company_data(company_username)
    
    if not company_data:
        return {
            "success": False,
            "message": "Could not fetch LinkedIn company data",
            "data": {}
        }
    
    return scraper.extract_company_information(company_data)

@router.post("/enriched-profile", response_model=None)
async def get_enriched_linkedin_profile(
    request: LinkedInProfileRequest,
    linkedin_scraper: LinkedInScraperService = Depends(LinkedInScraperService),
) -> Dict[str, Any]:
    """
    Fetch LinkedIn profile data and enrich it with company information
    """
    profile_data = await linkedin_scraper.get_profile_data(request.profile_url)
    if not profile_data:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    enriched_data = await linkedin_scraper.enrich_profile_with_company_data(
        profile_data, 
        request.focus_area,
        cleanup=request.cleanup
    )
    return enriched_data 