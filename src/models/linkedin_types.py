from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import date

class GeoLocation(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    full: Optional[str] = None
    countryCode: Optional[str] = None

class DateInfo(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None

class Education(BaseModel):
    start: Optional[DateInfo] = None
    end: Optional[DateInfo] = None
    fieldOfStudy: Optional[str] = None
    degree: Optional[str] = None
    grade: Optional[str] = None
    schoolName: Optional[str] = None
    description: Optional[str] = None
    activities: Optional[str] = None
    url: Optional[str] = None
    schoolId: Optional[str] = None

class MultiLocale(BaseModel):
    en_US: Optional[str] = None

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
    title: Optional[str] = None
    description: Optional[str] = None
    start: Optional[DateInfo] = None
    end: Optional[DateInfo] = None
    location: Optional[str] = None
    employmentType: Optional[str] = None
    companyName: Optional[str] = None
    extraInfo: Optional[CompanyExtraInfo] = None

class Skill(BaseModel):
    name: Optional[str] = None
    passedSkillAssessment: Optional[bool] = None
    endorsementsCount: Optional[int] = None

class BackgroundImage(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    url: Optional[str] = None

class SupportedLocale(BaseModel):
    country: Optional[str] = None
    language: Optional[str] = None

class MultiLocaleText(BaseModel):
    en: Optional[str] = None

class LinkedInProfileScraperResponse(BaseModel):
    id: Optional[int] = None
    urn: Optional[str] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    isTopVoice: Optional[bool] = None
    isCreator: Optional[bool] = None
    profilePicture: Optional[str] = None
    backgroundImage: List[BackgroundImage] = None
    summary: Optional[str] = None
    headline: Optional[str] = None
    geo: Optional[GeoLocation] = None
    educations: List[Education] = None
    positions: List[Position] = None
    fullPositions: List[Position] = None
    skills: List[Skill] = None
    projects: Dict = None
    supportedLocales: List[SupportedLocale] = None
    multiLocaleFirstName: Optional[MultiLocaleText] = None
    multiLocaleLastName: Optional[MultiLocaleText] = None
    multiLocaleHeadline: Optional[MultiLocaleText] = None

class Image(BaseModel):
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class Headquarter(BaseModel):
    geographicArea: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    postalCode: Optional[str] = None
    line1: Optional[str] = None

class CallToActionMessage(BaseModel):
    textDirection: Optional[str] = None
    text: Optional[str] = None

class CallToAction(BaseModel):
    callToActionType: Optional[str] = None
    visible: Optional[bool] = None
    callToActionMessage: Optional[CallToActionMessage] = None
    url: Optional[str] = None

class MoneyRaised(BaseModel):
    currencyCode: Optional[str] = None
    amount: Optional[str] = None

class AnnouncedOn(BaseModel):
    month: Optional[int] = None
    day: Optional[int] = None
    year: Optional[int] = None

class LastFundingRound(BaseModel):
    investorsCrunchbaseUrl: Optional[str] = None
    leadInvestors: Optional[List[Dict[str, str]]] = None
    fundingRoundCrunchbaseUrl: Optional[str] = None
    fundingType: Optional[str] = None
    moneyRaised: Optional[MoneyRaised] = None
    numOtherInvestors: Optional[int] = None
    announcedOn: Optional[AnnouncedOn] = None

class FundingData(BaseModel):
    updatedAt: Optional[str] = None
    updatedDate: Optional[str] = None
    numFundingRounds: Optional[int] = None
    lastFundingRound: Optional[LastFundingRound] = None

class LinkedInCompanyData(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    universalName: Optional[str] = None
    linkedinUrl: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    phone: Optional[str] = None
    investorsCrunchbaseUrl: Optional[str]
    leadInvestors: Optional[List[Dict[str, str]]]
    fundingRoundCrunchbaseUrl: Optional[str]
    fundingType: Optional[str]
    moneyRaised: Optional[MoneyRaised]
    numOtherInvestors: Optional[int]
    announcedOn: Optional[AnnouncedOn]

class FundingData(BaseModel):
    updatedAt: Optional[str]
    updatedDate: Optional[str]
    numFundingRounds: Optional[int]
    lastFundingRound: Optional[LastFundingRound]

class LinkedInCompanyData(BaseModel):
    id: Optional[str]
    name: Optional[str]
    universalName: Optional[str]
    linkedinUrl: Optional[str]
    tagline: Optional[str]
    description: Optional[str]
    type: Optional[str]
    phone: Optional[str]
    Images: Optional[Dict[str, str]]
    isClaimable: Optional[bool]
    backgroundCoverImages: Optional[List[Image]]
    logos: Optional[List[Image]]
    staffCount: Optional[int]
    headquarter: Optional[Headquarter]
    locations: Optional[List[Dict[str, Any]]]
    industries: Optional[List[str]]
    specialities: Optional[List[str]]
    website: Optional[str]
    founded: Optional[str]
    callToAction: Optional[CallToAction]
    followerCount: Optional[int]
    staffCountRange: Optional[str]
    crunchbaseUrl: Optional[str]
    fundingData: Optional[FundingData]

class LinkedInCompanyResponse(BaseModel):
    success: bool
    message: str
    data: Optional[LinkedInCompanyData]

class Geo(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    full: Optional[str] = None

class FullPosition(BaseModel):
    companyId: Optional[int] = None
    companyName: Optional[str] = None
    companyUsername: Optional[str] = None
    companyIndustry: Optional[str] = None
    companyStaffCountRange: Optional[str] = None
    title: Optional[str] = None
    multiLocaleTitle: Optional[MultiLocale] = None
    multiLocaleCompanyName: Optional[MultiLocale] = None
    location: Optional[str] = None
    description: Optional[str] = None
    employmentType: Optional[str] = None
    start: Optional[DateInfo] = None
    end: Optional[DateInfo] = None

class UserProfile(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    isTopVoice: Optional[bool] = None
    isCreator: Optional[bool] = None
    isPremium: Optional[bool] = None
    summary: Optional[str] = None
    headline: Optional[str] = None
    geo: Optional[Geo] = None
    educations: Optional[List[Education]] = None
    position: Optional[List[Position]] = None
    fullPositions: Optional[List[FullPosition]] = None
    skills: Optional[List[Skill]] = None
    projects: Optional[dict] = None
    supportedLocales: Optional[List[SupportedLocale]] = None
    multiLocaleFirstName: Optional[MultiLocaleText] = None
    multiLocaleLastName: Optional[MultiLocaleText] = None
    multiLocaleHeadline: Optional[MultiLocaleText] = None

class CleanedCompanyExtraInfo(BaseModel):
    headquarter: Optional[Dict[str, str]] = None
    locations: Optional[List[str]] = None
    industries: Optional[List[str]] = None
    specialities: Optional[List[str]] = None
    founded: Optional[str] = None
    followerCount: Optional[int] = None
    staffCountRange: Optional[str] = None
    fundingData: Optional[Dict[str, Any]] = None

class CleanedEducation(BaseModel):
    start: Optional[DateInfo] = None
    end: Optional[DateInfo] = None
    fieldOfStudy: Optional[str] = None
    degree: Optional[str] = None
    grade: Optional[str] = None
    schoolName: Optional[str] = None
    description: Optional[str] = None
    activities: Optional[str] = None
    schoolId: Optional[str] = None

class CleanedSkill(BaseModel):
    name: Optional[str] = None

class CleanedPosition(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start: Optional[DateInfo] = None
    end: Optional[DateInfo] = None
    location: Optional[str] = None
    employmentType: Optional[str] = None
    companyName: Optional[str] = None
    extraInfo: Optional[CleanedCompanyExtraInfo] = None

class CleanedLinkedInProfileScraperResponse(BaseModel):
    id: Optional[int] = None
    urn: Optional[str] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    isTopVoice: Optional[bool] = None
    isCreator: Optional[bool] = None
    summary: Optional[str] = None
    headline: Optional[str] = None
    geo: Optional[GeoLocation] = None
    educations: List[CleanedEducation] = []
    positions: List[CleanedPosition] = []
    fullPositions: List[CleanedPosition] = []
    skills: List[CleanedSkill] = []
    supportedLocales: List[SupportedLocale] = []
    multiLocaleFirstName: Optional[MultiLocaleText] = None
    multiLocaleLastName: Optional[MultiLocaleText] = None
    multiLocaleHeadline: Optional[MultiLocaleText] = None 