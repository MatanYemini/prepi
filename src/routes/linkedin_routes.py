from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.linkedin_scraper_service import LinkedInScraperService


router = APIRouter(prefix="/linkedin", tags=["linkedin"])

class linkedinProfileRequest(BaseModel):
    profile_url: str
    cleanup: bool = False
    include_posts: bool = False
    
@router.post("/profile", response_model=None)
async def get_linkedin_profile(request: linkedinProfileRequest):
    """
    Fetch LinkedIn profile data for a given profile URL
    """
    scraper = LinkedInScraperService()
    profile_data = await scraper.get_profile_data(str(request.profile_url), request.cleanup)
    
    if not profile_data:
        raise HTTPException(
            status_code=404,
            detail="Could not fetch LinkedIn profile data"
        )
    
    if request.include_posts:
        await scraper.add_posts_to_profile_data(profile_data)
    
    return JSONResponse(status_code=200, content=profile_data)
