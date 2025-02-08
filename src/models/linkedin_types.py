from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class GeoLocation(BaseModel):
    country: Optional[str]
    city: Optional[str]
    full: Optional[str]
    countryCode: Optional[str]

class DateInfo(BaseModel):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]

class Education(BaseModel):
    start: Optional[DateInfo]
    end: Optional[DateInfo]
    fieldOfStudy: Optional[str]
    degree: Optional[str]
    grade: Optional[str]
    schoolName: Optional[str]
    description: Optional[str]
    activities: Optional[str]
    url: Optional[str]
    schoolId: Optional[str]

class MultiLocale(BaseModel):
    en_US: Optional[str]

class CompanyExtraInfo(BaseModel):
    headquarter: Optional[Dict[str, str]] = None
    locations: Optional[List[str]] = None
    industries: Optional[List[str]] = None
    specialities: Optional[List[str]] = None
    website: Optional[str] = None
    founded: Optional[str] = None
    followerCount: Optional[int] = None
    staffCountRange: Optional[str] = None
    fundingData: Optional[Dict[str, Any]] = None

class Position(BaseModel):
    title: str
    description: Optional[str] = None
    start: Optional[Dict[str, Any]] = None
    end: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    employmentType: Optional[str] = None
    companyName: Optional[str] = None
    extraInfo: Optional[CompanyExtraInfo] = None

class Skill(BaseModel):
    name: Optional[str]
    passedSkillAssessment: Optional[bool]
    endorsementsCount: Optional[int]

class BackgroundImage(BaseModel):
    width: Optional[int]
    height: Optional[int]
    url: Optional[str]

class SupportedLocale(BaseModel):
    country: str
    language: str

class MultiLocaleText(BaseModel):
    en: Optional[str]

class LinkedInProfileResponse(BaseModel):
    id: Optional[int]
    urn: Optional[str]
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    isTopVoice: Optional[bool]
    isCreator: Optional[bool]
    profilePicture: Optional[str]
    backgroundImage: List[BackgroundImage] = []
    summary: Optional[str]
    headline: Optional[str]
    geo: Optional[GeoLocation]
    educations: List[Education] = []
    positions: List[Position]
    fullPositions: List[Position] = []
    skills: List[Skill] = []
    projects: Dict = {}
    supportedLocales: List[SupportedLocale] = []
    multiLocaleFirstName: Optional[MultiLocaleText]
    multiLocaleLastName: Optional[MultiLocaleText]
    multiLocaleHeadline: Optional[MultiLocaleText]

class LinkedInCompanyResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] 